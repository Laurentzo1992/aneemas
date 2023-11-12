import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    # Encode l'image en base64
    graph = base64.b64encode(image_png).decode('utf-8').strip()
    return graph




def get_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(3,3))
    #plt.title("Nombre d'accident")
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('periode')
    plt.ylabel('nombre')
    plt.tight_layout()
    graph = get_graph()
    return graph