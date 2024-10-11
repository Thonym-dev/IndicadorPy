from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Device
import networkx as nx
import plotly.graph_objects as go
import plotly.io as pio
from django.db.models import Sum, Max, Avg

# Create your views here.
def index(request):
    return render(request, 'index.html')

def inputs(request):
    context = {}
    devices = Device.objects.all()
    context['devices'] = devices
    if request.method == 'POST':
        device_type = request.POST.get('device_type', None)
        device_name = request.POST.get('device_name', None)
        interruptions = int(request.POST.get('interruptions', 0))
        resolution_time = float(request.POST.get('resolution_time', 0))
        connected_clients = int(request.POST.get('connected_clients', 0))

        if device_type and device_name:
            # Save to database
            new_device = Device(
                device_type=device_type,
                device_name=device_name,
                interruptions=interruptions,
                resolution_time=resolution_time,
                connected_clients=connected_clients
            )
            new_device.save()
        
        # After saving, retrieve all devices and render the inputs page
        devices = Device.objects.all()
        return render(request, 'inputs.html', {'devices': devices})
    
    # If not a POST, display the page with the device table
    devices = Device.objects.all()
    return render(request, 'inputs.html', {'devices': devices})

def show_graph(request):
    # Recupera todos os dispositivos do banco de dados
    devices = Device.objects.all()
    
    # Verifique se há dispositivos antes de gerar o grafo
    generate_graph(devices)  # Pass devices directly here  # Or generate a random graph if no devices exist
    return render(request, 'show_graph.html', {'json_path': 'static/graph.json'})

def generate_graph(devices):
    # Generate a random graph
    G = nx.DiGraph()

# Adding nodes for Substation, Transformers, Disconnectors, and Fuses
    G.add_edges_from([
        ('Substation', 'Transformer1'),
        ('Transformer1', 'Fuse1'),
        ('Fuse1', 'Disconnector1'),
        ('Disconnector1', 'Transformer2'),
        
        # Adding branches for further distribution (ramifications)
        ('Transformer2', 'Bar1'),
        ('Bar1', 'Fuse2'),
        ('Bar1', 'Disconnector2'),
        
        ('Disconnector2', 'Transformer3'),
        ('Fuse2', 'Transformer4'),

        # Extending the network with more ramifications
        ('Transformer3', 'Bar2'),
        ('Transformer4', 'Bar3'),
        ('Bar2', 'Fuse3'),
        ('Bar3', 'Disconnector3')
    ])

    # Get node positions using spring layout for better visualization
    pos = nx.spring_layout(G)

    # Create a Plotly trace for the edges
    edge_trace = go.Scatter(
        x=(),  # Initialize as tuple
        y=(),
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Add positions for each edge
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)  # Tuple concatenation
        edge_trace['y'] += (y0, y1, None)

    # Create a trace for the nodes
    node_trace = go.Scatter(
        x=(),
        y=(),
        text=[],  # Initialize as an empty list
        mode='markers+text',
        hoverinfo='text',
        marker=dict(showscale=False, color='skyblue', size=30, line_width=2))

    # List to hold node names
    node_texts = []

    # Add positions and text for each node
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)  # Tuple concatenation
        node_trace['y'] += (y,)
        node_texts.append(node)  # Append node name to the list

    # Assign the node_texts list back to node_trace['text']
    node_trace['text'] = node_texts


    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False))
                    )

    print(node_trace, edge_trace)

    fig.write_json('static/graph.json')


def calculate_indicators():
    devices = Device.objects.all()

    total_interruption_time = devices.aggregate(Sum('resolution_time'))['resolution_time__sum'] or 0
    total_interruptions = devices.aggregate(Sum('interruptions'))['interruptions__sum'] or 0
    dic = total_interruption_time / total_interruptions if total_interruptions > 0 else 0

    total_clients_connected = devices.aggregate(Sum('connected_clients'))['connected_clients__sum'] or 0
    fic = total_interruptions / total_clients_connected if total_clients_connected > 0 else 0
    dec = total_interruption_time / total_clients_connected if total_clients_connected > 0 else 0
    fec = total_interruptions / total_clients_connected if total_clients_connected > 0 else 0
    dmic = devices.aggregate(Max('resolution_time'))['resolution_time__max'] or 0

    return {
        'DIC': dic,
        'FIC': fic,
        'DEC': dec,
        'FEC': fec,
        'DMIC': dmic
    }

def indicators_view(request):
    indicators = calculate_indicators()
    return render(request, 'indicators.html', {'indicators': indicators})
