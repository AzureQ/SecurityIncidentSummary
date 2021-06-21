import pandas as pd
import functools
from flask import current_app


def pre_process(incident_lists, incident_types, identity_lists):
    id_col = current_app.config.get('ELEVATE_IDENTIFIER_COL')
    incident_priorities = current_app.config.get('ELEVATE_INCIDENT_PRIORITIES')
    identities = identity_lists[0]
    processed = []
    # Convert all incidents into a list of records with same structure like:
    #       {
    #         "employee_id":'4506"
    #         "low": {
    #             "count": 0,
    #             "incidents": []
    #         }
    #         "medium": {
    #             "count": 3,
    #             "incidents": [ ... ]
    #         }
    #         ...
    #     }
    for idx, incident_type in enumerate(incident_types):
        incidents = incident_lists[idx]['results']
        for inc in incidents:
            record = {}
            inc['type'] = incident_type
            record.update(inc)

            record['employee_id'] = identity_lookup(inc[id_col[incident_type]], identities)

            priorities = {p: {'count': 0, 'incidents': []} for p in incident_priorities}
            priorities.update({inc['priority']: {'count': 1, 'incidents': [inc]}})
            record.update(priorities)

            processed.append(record)
    return processed


# Helper function for replacing IP with employee_id
def identity_lookup(identifier, look_up_tbl):
    if identifier in look_up_tbl:
        return look_up_tbl[identifier]
    return identifier


def aggregate_by_emp_priority(incidents):
    df = pd.DataFrame(incidents)
    df = df.groupby('employee_id').pipe(aggr_by_priority)
    return df


def aggr_by_priority(grouped):
    # for each group:
    #   1. sum up 'count'
    #   2.concat & sort 'incidents'
    def aggr_count_and_incidents(series):
        return functools.reduce(lambda x, y: {'count': x['count'] + y['count'],
                                              'incidents': sorted(x['incidents'] + y['incidents'],
                                                                  key=lambda i: i['timestamp'])},
                                series)

    # Aggregate within each employee group by priority
    df = grouped.aggregate({k: aggr_count_and_incidents for k in ['low', 'medium', 'high', 'critical']})
    return df
