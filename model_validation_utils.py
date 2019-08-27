import pandas as pd

def get_plot_samples(ia_threshold, sim_reqs_eventG, trace_timeouts):

    filtered_reqs_eventG = sim_reqs_eventG.ia_timeout \
        [(sim_reqs_eventG.ia_timeout < ia_threshold)]
    filtered_reqs_traceB = trace_timeouts \
        [(trace_timeouts < ia_threshold)]

    n_samples = min([len(filtered_reqs_eventG), len(filtered_reqs_traceB)])
    # n_samples = 5000

    eventG_ia_samples = \
        filtered_reqs_eventG \
            .sample(n_samples).sort_values()

    traceB_ia_samples = \
        filtered_reqs_traceB \
            .sample(n_samples).sort_values()

    return eventG_ia_samples, traceB_ia_samples

def get_grouped_reqs_count(group_col, sim_reqs_eventG, sim_reqs_traceB):
    sim_reqs_eventG_count = \
        pd.Series((sim_reqs_eventG\
                   .sort_values("start_time")\
                   .groupby(group_col).origin_id.count()), name="eventG")

    sim_reqs_traceB_count = \
        pd.Series((sim_reqs_traceB\
                   .sort_values("start_time")\
                   .groupby(group_col).origin_id.count()), name="traceB")

    return sim_reqs_eventG_count, sim_reqs_traceB_count
