import plotly.graph_objects as go

def render_multi_metric_heatmap(metric_grids, x_coords, z_coords, customdata=None, customdata_metric=None):
    """metric_grids: dict of metric_name -> grid (all same shape/coords).
    customdata: optional array of extra per-cell data, shaped like the grids.
    customdata_metric: which metric name in metric_grids should use customdata
    for a richer hover template."""
    metric_names = list(metric_grids.keys())

    fig = go.Figure()
    for i, name in enumerate(metric_names):
        if name == customdata_metric and customdata is not None:
            fig.add_trace(go.Heatmap(
                z=metric_grids[name],
                x=x_coords,
                y=z_coords,
                customdata=customdata,
                colorscale='Viridis',
                visible=(i == 0),
                colorbar=dict(title=name),
                hovertemplate=(
                    'Chunk (%{x}, %{y})<br>'
                    'Air: %{z:.1f}%<br>'
                    'Solid: %{customdata[0]:.1f}%<br>'
                    'Liquid: %{customdata[1]:.1f}<br>'
                    'Cave Air: %{customdata[2]:.1f}<extra></extra>'
                )
            ))
        else:
            fig.add_trace(go.Heatmap(
                z=metric_grids[name],
                x=x_coords,
                y=z_coords,
                colorscale='Viridis',
                visible=(i == 0),
                colorbar=dict(title=name)
            ))

    buttons = []
    for i, name in enumerate(metric_names):
        visibility = [j == i for j in range(len(metric_names))]
        buttons.append(dict(
            label=name,
            method='update',
            args=[{'visible': visibility}, {'title': f'{name} Heatmap'}]
        ))

    fig.update_layout(
        updatemenus=[dict(active=0, buttons=buttons, x=1.15, y=1.15)],
        title=f'{metric_names[0]} Heatmap',
        xaxis_title='Chunk X',
        yaxis_title='Chunk Z'
    )

    fig.write_html('results/figures/combined_heatmap.html')
    return fig