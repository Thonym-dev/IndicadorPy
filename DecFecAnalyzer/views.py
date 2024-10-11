from django.shortcuts import render,  redirect
from django.http import HttpResponse
from .models import Device
import networkx as nx
import plotly.graph_objects as go


# Create your views here.
def index(request):
    return render(request, 'index.html')

def inputs(request):
    return render(request, 'inputs.html')

def generate_graph(devices):
    G = nx.Graph()

    for device in devices:
        # Adiciona os nós ao grafo
        G.add_node(device.device_name, type=device.device_type)

    # Criando as arestas (você pode definir a lógica de conexão entre os dispositivos aqui)
    for i in range(len(devices)-1):
        G.add_edge(devices[i].device_name, devices[i+1].device_name)

    # Gerar a visualização do grafo usando Plotly
    pos = nx.spring_layout(G)  # Layout dos nós

    edge_trace = go.Scatter(
        x=[], y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = go.Scatter(
        x=[], y=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Dispositivos',
                xanchor='left',
                titleside='right'),
        )
    )

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += [x]
        node_trace['y'] += [y]
        node_trace['text'] += [f"{node} - {G.nodes[node]['type']}"]

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))

    # Salvar a imagem do grafo
    fig.write_image("static/graph.png")

# View para salvar o dispositivo e renderizar o grafo
def save_device(request):
    if request.method == 'POST':
        device_type = request.POST['device_type']
        device_name = request.POST['device_name']
        interruptions = int(request.POST['interruptions'])
        resolution_time = float(request.POST['resolution_time'])
        connected_clients = int(request.POST['connected_clients'])

        # Salvando no banco de dados
        new_device = Device(
            device_type=device_type,
            device_name=device_name,
            interruptions=interruptions,
            resolution_time=resolution_time,
            connected_clients=connected_clients
        )
        new_device.save()

        # Recupera todos os dispositivos e gera o grafo
        all_devices = Device.objects.all()
        generate_graph(all_devices)

        # Redireciona para a página que mostra o grafo
        return render(request, 'show_graph.html')

    return render(request, 'inputs.html')