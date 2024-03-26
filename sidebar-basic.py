import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# 명령어 그룹 정의
commands = {
    'Basic Commands (Beginner)': {
        'create': 'Create a resource from a file or from stdin',
        'expose': 'Expose it as a new Kubernetes service',
        'run': 'Run a particular image on the cluster',
        'set': 'Set specific features on objects'
    },
    'Basic Commands (Intermediate)': {
        'explain': 'Get documentation for a resource',
        'get': 'Display one or many resources',
        'edit': 'Edit a resource on the server',
        'delete': 'Delete resources by various methods'
    },
    'Deploy Commands': {
        'rollout': 'Manage the rollout of a resource',
        'scale': 'Set a new size for a deployment, replica set, or replication controller',
        'autoscale': 'Auto-scale a deployment, replica set, stateful set, or replication controller'
    },
    'Cluster Management Commands': {
        'certificate': 'Modify certificate resources',
        'cluster-info': 'Display cluster information',
        'top': 'Display resource (CPU/memory) usage',
        'cordon': 'Mark node as unschedulable',
        'uncordon': 'Mark node as schedulable',
        'drain': 'Drain node in preparation for maintenance',
        'taint': 'Update the taints on one or more nodes'
    },
    'Troubleshooting and Debugging Commands': {
        'describe': 'Show details of a specific resource or group of resources',
        'logs': 'Print the logs for a container in a pod',
        'attach': 'Attach to a running container',
        'exec': 'Execute a command in a container',
        'port-forward': 'Forward one or more local ports to a pod',
        'proxy': 'Run a proxy to the Kubernetes API server',
        'cp': 'Copy files and directories to and from containers',
        'auth': 'Inspect authorization',
        'debug': 'Create debugging sessions for troubleshooting workloads and nodes',
        'events': 'List events'
    },
    'Advanced Commands': {
        'diff': 'Diff the live version against a would-be applied version',
        'apply': 'Apply a configuration to a resource by file name or stdin',
        'patch': 'Update fields of a resource',
        'replace': 'Replace a resource by file name or stdin',
        'wait': 'Wait for a specific condition on one or many resources',
        'kustomize': 'Build a kustomization target from a directory or URL'
    },
    'Settings Commands': {
        'label': 'Update the labels on a resource',
        'annotate': 'Update the annotations on a resource',
        'completion': 'Output shell completion code for the specified shell (bash, zsh, fish, or powershell)'
    },
    'Other Commands': {
        'api-resources': 'Print the supported API resources on the server',
        'api-versions': 'Print the supported API versions on the server, in the form of "group/version"',
        'config': 'Modify kubeconfig files',
        'plugin': 'Provides utilities for interacting with plugins',
        'version': 'Print the client and server version information'
    }
}


app.layout = html.Div([
    # Sidebar
    html.Div([
        html.H2('명령어 그룹', style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='command-group-dropdown',
            options=[{'label': group, 'value': group} for group in commands.keys()],
            value=list(commands.keys())[0],
        ),
        # Add other sidebar elements here
    ], style={
        'width': '20%',
        'float': 'left',
        'display': 'inline-block',
        'background-color': '#f8f9fa',  # Light grey background
        'padding': '20px',
        'height': '100vh',  # Full height of the viewport
        'box-shadow': '2px 0px 5px 0px rgba(0,0,0,0.1)'  # Adding some shadow for depth
    }),

    # Main content area
    html.Div([
        html.H2('명령어 상세'),
        dcc.Dropdown(id='command-dropdown'),
        html.Div(id='command-description'),
    ], style={
        'width': '70%',
        'float': 'right',
        'display': 'inline-block',
        'padding': '20px'
    }),
])

# Add your callbacks here

if __name__ == '__main__':
    app.run_server(debug=True)
