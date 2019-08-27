import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
matplotlib.rcParams["axes.grid"] = True
matplotlib.rcParams["figure.figsize"] = (15., 7.)

from model_validation_utils import get_plot_samples
from model_validation_utils import get_grouped_reqs_count

def plot_ia_validation(ia_threshold, city, sim_reqs_eventG, trace_timeouts):

    eventG_ia_samples, traceB_ia_samples = \
        get_plot_samples(ia_threshold, sim_reqs_eventG, trace_timeouts)

    plt.figure(figsize=(9, 9))
    plt.title("Q-q plot of interarrival times")
    plt.scatter(eventG_ia_samples, traceB_ia_samples)
    plt.plot(eventG_ia_samples.sort_values(),
             eventG_ia_samples.sort_values())
    plt.xlabel("sim ia times")
    plt.ylabel("trace ia times [s]")
    plt.savefig("./Figures/" + city + "/validation/qq-" + str(ia_threshold))
    plt.show()
    plt.close()

def plot_tot_reqs_count(group_col, normed, city, sim_reqs_eventG, sim_reqs_traceB):
    sim_reqs_eventG_count, sim_reqs_traceB_count = \
        get_grouped_reqs_count(group_col, sim_reqs_eventG, sim_reqs_traceB)

    if normed:
        title = "normalised"
        figfilename = "_".join([group_col, "reqs-count-norm"])
        sim_reqs_eventG_count = \
            sim_reqs_eventG_count / len(sim_reqs_eventG)
        sim_reqs_traceB_count = \
            sim_reqs_traceB_count / len(sim_reqs_traceB)
    else:
        title = ""
        figfilename = "_".join([group_col, "reqs-count"])

    plt.figure(figsize=(15, 7))
    pd.concat([sim_reqs_eventG_count,
               sim_reqs_traceB_count], axis=1) \
        .plot.bar()
    plt.title(title + " count of booking requests by " + group_col)
    plt.xlabel(group_col)
    plt.ylabel("% booking requests")
    plt.legend()
    plt.savefig("./Figures/" + city + "/validation/" + figfilename)
    plt.show()
    plt.close()


def plot_tot_reqs_count_err(group_col, normed, city, sim_reqs_eventG, sim_reqs_traceB):
    sim_reqs_eventG_count = \
        (sim_reqs_eventG \
         .sort_values("start_time") \
         .groupby(group_col).origin_id.count())

    sim_reqs_traceB_count = \
        (sim_reqs_traceB \
         .sort_values("start_time") \
         .groupby(group_col).origin_id.count())

    if normed:
        title = "normalised"
        figfilename = "_".join([group_col, "reqs-count-err-norm"])
        sim_reqs_eventG_count = \
            sim_reqs_eventG_count / len(sim_reqs_eventG)
        sim_reqs_traceB_count = \
            sim_reqs_traceB_count / len(sim_reqs_traceB)
    else:
        title = ""
        figfilename = "_".join([group_col, "reqs-count"])

    print("Total error:",
          (sim_reqs_eventG_count - sim_reqs_traceB_count).abs().sum())

    plt.figure(figsize=(15, 7))
    (sim_reqs_eventG_count - sim_reqs_traceB_count).abs() \
        .plot.bar()
    plt.title(title + " count error by " + group_col)
    plt.xlabel(group_col)
    plt.ylabel("% booking requests")
    plt.savefig("./Figures/" + city + "/validation/" + figfilename)
    plt.show()
    plt.close()


def plot_tot_reqs_count_err_agg(group_col, normed, city, sim_reqs_eventG, sim_reqs_traceB):
    sim_reqs_eventG_count = \
        (sim_reqs_eventG \
         .sort_values("start_time") \
         .groupby(["daytype", "hour"]).origin_id.count())

    sim_reqs_traceB_count = \
        (sim_reqs_traceB \
         .sort_values("start_time") \
         .groupby(["daytype", "hour"]).origin_id.count())

    if normed:
        title = "normalised"
        figfilename = "_".join(["reqs-count-err-norm"])
        sim_reqs_eventG_count = \
            sim_reqs_eventG_count / len(sim_reqs_eventG)
        sim_reqs_traceB_count = \
            sim_reqs_traceB_count / len(sim_reqs_traceB)
    else:
        title = ""
        figfilename = "_".join(["reqs-count-err"])

    print("Total error:",
          (sim_reqs_eventG_count - sim_reqs_traceB_count).abs().sum())

    spatial_errs_df = pd.DataFrame()
    for daytype in ["weekday", "weekend"]:
        spatial_errs_df[daytype] = \
            sim_reqs_eventG_count.loc[daytype] \
            - sim_reqs_traceB_count.loc[daytype]

    plt.figure(figsize=(15, 7))
    (spatial_errs_df).abs() \
        .plot.bar(figsize=(15, 7))
    plt.title(title + " count error by hour and daytype")
    plt.xlabel("hour")
    plt.ylabel("% booking requests")
    plt.savefig("./Figures/" + city + "/validation/" + figfilename)
    plt.show()
    plt.close()