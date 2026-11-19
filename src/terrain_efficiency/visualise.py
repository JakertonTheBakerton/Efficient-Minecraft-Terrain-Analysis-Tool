import plotly.graph_objects as go

def render_multi_metric_heatmap(metric_grids, x_coords, z_coords, customdata=None, customdata_metric=None):
    """metric_grids: dict of metric_name -> grid (all same shape/coords).
    layer_configs: optional dict of metric_name -> {'customdata': array, 'hovertemplate': str}."""
    metric_names = list(metric_grids.keys())
    
    if layer_configs is None:
        layer_configs = {}
    
    fig = go.Figure()
    for i, name in enumerate(metric_names):
        config = layer_configs.get(name, {})
        
        # Start with the base arguments
        trace_args = dict(
            z=metric_grids[name],
            x=x_coords,
            y=z_coords,
            colorscale='Viridis',
            visible=(i == 0),
            colorbar=dict(title=name)
        )
        
        # Add customdata and hovertemplate if this layer has them
        if 'customdata' in config:
            trace_args['customdata'] = config['customdata']
        if 'hovertemplate' in config:
            trace_args['hovertemplate'] = config['hovertemplate']
            
        fig.add_trace(go.Heatmap(**trace_args))

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
