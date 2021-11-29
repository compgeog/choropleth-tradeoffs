import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

def pcpx(data, style=None, bounds=None, labels=None, legend_labels=None, legend_loc='upper right', bbox_to_anchor=None):
    """
    Parallel coordinate plots - NCX
    TODO: scale on each vertical axis, ticks on inner axes
    """
    dims = len(data[0])
    x    = range(dims)
    #fig, axes = plt.subplots(1, dims-1, sharey=False)
    ax = plt.gca()
#     ax.set_axis_bgcolor('white')
    if style is None:
        style = ['r-']*len(datas)
    # Calculate the limits on the data
    min_max_range = list()
    if bounds is not None:
        min_max_range = [(b[0], b[1], float(b[1]-b[0])) for b in bounds]
    else:
        for m in zip(*data):
            mn, mx = min(m), max(m)
            if mn == mx:
                mn -= 0.5
                mx = mn + 1.
            r  = float(mx - mn)
            min_max_range.append((mn, mx, r))
    ax.set_ylim(min_max_range[0][0], min_max_range[0][1])
    # Plot the datasets
    current_style = None
    for dsi, d in enumerate(data):
        if style[dsi] is not current_style and legend_labels is not None:
            plt.plot(x, d, style[dsi], label=legend_labels[dsi])
            current_style = style[dsi]
        else:
            plt.plot(x, d, style[dsi])
    if legend_labels is not None:
        plt.legend(frameon=False, loc=legend_loc, bbox_to_anchor=bbox_to_anchor)
    plt.xticks(x)
    for xx in x:
        ax.axvline(xx, color='k', linestyle='-')
    if labels is not None:
        ax.set_xticklabels(labels)
    return plt


def pcpx_other(data, style=None, bounds=None, labels=None, legend_labels=None, legend_loc='upper right', bbox_to_anchor=None):
    """
    Parallel coordinate plots - NCX
    TODO: scale on each vertical axis, ticks on inner axes
    """
    dims = len(data[0])
    x    = range(dims)
    #fig, axes = plt.subplots(1, dims-1, sharey=False)
    ax = plt.gca()
#     ax.set_axis_bgcolor('white')
    if style is None:
        style = ['r-']*len(datas)
    # Calculate the limits on the data
    min_max_range = list()
    if bounds is not None:
        min_max_range = [(b[0], b[1], float(b[1]-b[0])) for b in bounds]
    else:
        for m in zip(*data):
            mn, mx = min(m), max(m)
            if mn == mx:
                mn -= 0.5
                mx = mn + 1.
            r  = float(mx - mn)
            min_max_range.append((mn, mx, r))
    ax.set_ylim(min_max_range[0][0], min_max_range[0][1])
    # Plot the datasets
    current_style = None
    for dsi, d in enumerate(data):
        if style[dsi] is not current_style and legend_labels is not None:
            plt.plot(x, d, style[dsi], label=legend_labels[dsi])
            current_style = style[dsi]
        else:
            plt.plot(x, d, style[dsi])
    if legend_labels is not None:
        plt.legend(frameon=False, loc=legend_loc, bbox_to_anchor=bbox_to_anchor)
    plt.xticks(x)
    for xx in x:
        ax.axvline(xx, color='k', linestyle='-')
    if labels is not None:
        ax.set_xticklabels(labels)
    return plt




def parallel_coordinates(data_sets, style=None):

    dims = len(data_sets[0])
    x    = range(dims)
    fig, axes = plt.subplots(1, dims-1, sharey=False)

    if style is None:
        style = ['r-']*len(data_sets)

    # Calculate the limits on the data
    min_max_range = list()
    for m in zip(*data_sets):
        mn = min(m)
        mx = max(m)
        if mn == mx:
            mn -= 0.5
            mx = mn + 1.
        r  = float(mx - mn)
        min_max_range.append((mn, mx, r))

    # Normalize the data sets
    norm_data_sets = list()
    for ds in data_sets:
        nds = [(value - min_max_range[dimension][0]) / 
                min_max_range[dimension][2] 
                for dimension,value in enumerate(ds)]
        norm_data_sets.append(nds)
    data_sets = norm_data_sets

    # Plot the datasets on all the subplots
    for i, ax in enumerate(axes):
        for dsi, d in enumerate(data_sets):
            ax.plot(x, d, style[dsi])
        ax.set_xlim([x[i], x[i+1]])

        
    # Set the x axis ticks 
    for dimension, (axx,xx) in enumerate(zip(axes, x[:-1])):
        axx.xaxis.set_major_locator(ticker.FixedLocator([xx]))
        ticks = len(axx.get_yticklabels())
        labels = list()
        step = min_max_range[dimension][2] / (ticks - 1)
        mn   = min_max_range[dimension][0]
        for i in xrange(ticks):
            v = mn + i*step
            labels.append('%4.2f' % v)
        axx.set_yticklabels(labels)


    # Move the final axis' ticks to the right-hand side
    axx = plt.twinx(axes[-1])
    dimension += 1
    axx.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
    ticks = len(axx.get_yticklabels())
    step = min_max_range[dimension][2] / (ticks - 1)
    mn   = min_max_range[dimension][0]
    labels = ['%4.2f' % (mn + i*step) for i in xrange(ticks)]
    axx.set_yticklabels(labels)

    # Stack the subplots 
    plt.subplots_adjust(wspace=0)

    # return plt


def parallel_coordinates_x(data_sets, style=None, bounds=None):

    dims = len(data_sets[0])
    x    = range(dims)
    fig, axes = plt.subplots(1, dims-1, sharey=False)

    if style is None:
        style = ['r-']*len(data_sets)

    # Calculate the limits on the data
    min_max_range = list()
    if bounds is not None:
        min_max_range = [(b[0], b[1], float(b[1]-b[0])) for b in bounds]
    else:
        for m in zip(*data_sets):
            mn = min(m)
            mx = max(m)
            if mn == mx:
                mn -= 0.5
                mx = mn + 1.
            r  = float(mx - mn)
            min_max_range.append((mn, mx, r))

    print('orig', data_sets)
        
    # Normalize the data sets
    norm_data_sets = list()
    for ds in data_sets:
        nds = [(value - min_max_range[dimension][0]) / 
                min_max_range[dimension][2] 
                for dimension,value in enumerate(ds)]
        norm_data_sets.append(nds)
    #data_sets = norm_data_sets

    print('norm:', data_sets)
    
    # Plot the datasets on all the subplots
    for i, ax in enumerate(axes):
        for dsi, d in enumerate(data_sets):
            ax.plot(x, d, style[dsi])
        ax.set_xlim([x[i], x[i+1]])

        
    # Set the x axis ticks 
    for dimension, (axx,xx) in enumerate(zip(axes, x[:-1])):
        axx.xaxis.set_major_locator(ticker.FixedLocator([xx]))
        ticks = len(axx.get_yticklabels())
        labels = list()
        step = min_max_range[dimension][2] / (ticks - 1)
        mn   = min_max_range[dimension][0]
        for i in xrange(ticks):
            v = mn + i*step
            labels.append('%4.2f' % v)
        axx.set_yticklabels(labels)


    # Move the final axis' ticks to the right-hand side
    axx = plt.twinx(axes[-1])
    dimension += 1
    axx.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
    ticks = len(axx.get_yticklabels())
    step = min_max_range[dimension][2] / (ticks - 1)
    mn   = min_max_range[dimension][0]
    labels = ['%4.2f' % (mn + i*step) for i in xrange(ticks)]
    axx.set_yticklabels(labels)

    # Stack the subplots 
    plt.subplots_adjust(wspace=0)

    # return plt
