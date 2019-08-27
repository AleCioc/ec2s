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

def get_day_moments (sim_reqs_eventG, sim_reqs_traceB):

    sim_reqs_eventG.loc \
        [(sim_reqs_eventG.hour.isin([23, 0, 1, 2, 3, 4])), "daymoment"] = "night"

    sim_reqs_eventG.loc \
        [(sim_reqs_eventG.hour.isin([5, 6, 7, 8, 9, 10, 11, 12])), "daymoment"] = "morning"

    sim_reqs_eventG.loc \
        [(sim_reqs_eventG.hour.isin([13, 14, 15, 16, 17, 18])), "daymoment"] = "afternoon"

    sim_reqs_eventG.loc \
        [(sim_reqs_eventG.hour.isin([19, 20, 21, 22])), "daymoment"] = "evening"

    sim_reqs_traceB.loc \
        [(sim_reqs_traceB.hour.isin([23, 0, 1, 2, 3, 4])), "daymoment"] = "night"

    sim_reqs_traceB.loc \
        [(sim_reqs_traceB.hour.isin([5, 6, 7, 8, 9, 10, 11, 12])), "daymoment"] = "morning"

    sim_reqs_traceB.loc \
        [(sim_reqs_traceB.hour.isin([13, 14, 15, 16, 17, 18])), "daymoment"] = "afternoon"

    sim_reqs_traceB.loc \
        [(sim_reqs_traceB.hour.isin([19, 20, 21, 22])), "daymoment"] = "evening"

    return sim_reqs_eventG, sim_reqs_traceB


def get_od_err(grid, sim_reqs_eventG, sim_reqs_traceB):

    for daymoment in ["night", "morning", "afternoon", "evening"]:
        grid["eventG_origin_count_" + daymoment] = \
            sim_reqs_eventG[sim_reqs_eventG.daymoment == daymoment] \
                .origin_id.value_counts() \
            / len(sim_reqs_eventG[sim_reqs_eventG.daymoment == daymoment])

        grid["traceB_origin_count_" + daymoment] = \
            sim_reqs_traceB[sim_reqs_traceB.daymoment == daymoment] \
                .origin_id.value_counts() \
            / len(sim_reqs_eventG[sim_reqs_eventG.daymoment == daymoment])

        grid["eventG_destination_count_" + daymoment] = \
            sim_reqs_eventG[sim_reqs_eventG.daymoment == daymoment] \
                .destination_id.value_counts() \
            / len(sim_reqs_eventG[sim_reqs_eventG.daymoment == daymoment])

        grid["traceB_destination_count_" + daymoment] = \
            sim_reqs_traceB[sim_reqs_traceB.daymoment == daymoment] \
                .destination_id.value_counts() \
            / len(sim_reqs_eventG[sim_reqs_eventG.daymoment == daymoment])

        grid["eventG_od_count_diff_" + daymoment] = \
            grid["eventG_origin_count_" + daymoment] \
            - grid["eventG_destination_count_" + daymoment]

        grid["traceB_od_count_diff_" + daymoment] = \
            grid["traceB_origin_count_" + daymoment] \
            - grid["traceB_destination_count_" + daymoment]

        current_grid = grid.loc \
            [:, ["eventG_od_count_diff_" + daymoment,
                 "traceB_od_count_diff_" + daymoment]] \
            .dropna(how="all").fillna(0)

        grid["od_count_diff_" + daymoment] = \
            current_grid["eventG_od_count_diff_" + daymoment] \
            - current_grid["traceB_od_count_diff_" + daymoment]

    return grid

def get_hourly_daytype_od_err(grid, sim_reqs_eventG, sim_reqs_traceB):
    mi_eventG_origin_count = \
        sim_reqs_eventG.groupby(["daytype", "hour"]) \
            .origin_id.value_counts()

    mi_traceB_origin_count = \
        sim_reqs_traceB.groupby(["daytype", "hour"]) \
            .origin_id.value_counts()

    mi_eventG_destination_count = \
        sim_reqs_eventG.groupby(["daytype", "hour"]) \
            .destination_id.value_counts()

    mi_traceB_destination_count = \
        sim_reqs_traceB.groupby(["daytype", "hour"]) \
            .destination_id.value_counts()

    spatial_errs_df = pd.DataFrame()

    for daytype in ["weekday", "weekend"]:

        spatial_errs_df[daytype] = pd.Series(index=range(24))

        for hour in range(24):
            mi_eventG_od_count_diff = \
                mi_eventG_origin_count.loc[daytype, hour] \
                - mi_eventG_destination_count.loc[daytype, hour]

            mi_traceB_od_count_diff = \
                mi_traceB_origin_count.loc[daytype, hour] \
                - mi_traceB_destination_count.loc[daytype, hour]

            current_grid = pd.concat \
                ([mi_eventG_od_count_diff,
                  mi_traceB_od_count_diff], axis=1) \
                .dropna(how="all").fillna(0)

            grid["od_count_diff_" + daytype + "_" + str(hour)] = \
                current_grid[0] - current_grid[1]

            spatial_errs_df.loc[hour, daytype] = \
                grid["od_count_diff_" + daytype + "_" + str(hour)].sum()

    return spatial_errs_df