import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import subprocess

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # bootstrap 적용

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

def run_kubectl_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        output = stdout.decode('utf-8')
    else:
        output = stderr.decode('utf-8')

    return output.strip()

app.layout = dbc.Container([

    # Title : kubectl 명령어 실행
    html.H2('kubectl 명령어 실행기', style={
        'backgroundColor': '#2D64FF',
        'color': 'white',
        'borderRadius': '20px',
        'textAlign': 'center',
        'padding': '10px',
        'fontSize': '1.5rem',
        'fontFamily': 'sans-serif',
        'fontWeight': 'bold',
        'display': 'inline-block',
        'marginTop': '5rem',
        'marginBottom': '1rem',
        'width': '100%'
    }, ),


    # command-input, execute-button, reset-button
    dbc.Row([
        dbc.Input(id='user-command-input', type='text', placeholder='kubectl 명령어를 입력하세요.', className="mb-2",
                  style={'width': '50%', 'marginLeft': '10px', 'marginRight': '10px', 'fontSize': '1rem', 'padding': '10px'}),
        dbc.Button('명령어 실행', id='execute-button', color='primary',
                   style={'width': '10%', 'fontSize': '1rem', 'padding': '10px', 'borderRadius': '5px',
                          'marginRight': '10px'}),
        dbc.Button('초기화', id='reset-button', color='secondary',
                   style={'width': '10%', 'fontSize': '1rem',  'padding': '10px', 'borderRadius': '5px'}),
        html.Br(), html.Br(),  # 두 줄 띄우기
        # 노드 조회 버튼 추가
        dcc.Loading(
            id="loading-query-nodes",  # 스피너의 고유 ID
            type="default",  # 스피너 타입
            children=[  # 스피너가 활성화될 동안 표시될 컴포넌트들
                dbc.Button(
                    html.Div([
                        "노드 조회",  # 첫 번째 줄 텍스트
                        html.Br(),  # 줄바꿈
                        "(kubectl get nodes)"  # 두 번째 줄 텍스트
                    ]),
                    id='get-nodes-button',
                    color='info',
                    style={'width': '10%', 'fontSize': '1rem', 'padding': '10px', 'marginRight': '10px'}
                ),

                dbc.Button(
                    html.Div([
                        "서비스 조회",  # 첫 번째 줄 텍스트
                        html.Br(),  # 줄바꿈
                        "(kubectl get svc -A)"  # 두 번째 줄 텍스트
                    ]),
                    id='get-svc-button',
                    color='info',
                    style={'width': '10%', 'fontSize': '1rem', 'padding': '10px', 'marginRight': '10px'}
                ),

                dbc.Button(
                    html.Div([
                        "네임스페이스 조회",  # 첫 번째 줄 텍스트
                        html.Br(),  # 줄바꿈
                        "(kubectl get ns)"  # 두 번째 줄 텍스트
                    ]),
                    id='get-ns-button',
                    color='info',
                    style={'width': '10%', 'fontSize': '1rem', 'padding': '10px', 'marginRight': '10px'}
                ),
            ],
            style={'display': 'inline-block'}  # 버튼을 인라인으로 표시
        ),
        html.Br(),  # 한 줄 띄우기
        # CardBody : user-command-result
        html.Div([
            dbc.Card(dbc.CardBody(id='user-command-result'),
                     style={'width': '100%', 'borderRadius': '5px'}),
        ]),


    ]),
    dbc.Row([
            dbc.Col(
                html.H4("Top 20 kubectl 명령어", className="text-center mt-4"),
                width=6
            ),
            dbc.Col(
                html.H4("K8s 리소스 타입 약자", className="text-center mt-4"),
                width=6
            )
        ]),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Ul([
                        html.Li(command) for command in [
                            "kubectl get nodes - 클러스터의 모든 노드를 나열합니다.",
                            "kubectl get pods - 현재 네임스페이스의 모든 파드를 나열합니다.",
                            "kubectl apply -f [파일명] - 구성 파일을 사용하여 리소스를 생성하거나 업데이트합니다.",
                            "kubectl delete pod [파드명] - 특정 파드를 삭제합니다.",
                            "kubectl get services - 현재 네임스페이스의 모든 서비스를 나열합니다.",
                            "kubectl describe pod [파드명] - 특정 파드에 대한 상세 정보를 보여줍니다.",
                            "kubectl logs [파드명] - 특정 파드의 로그를 출력합니다.",
                            "kubectl exec -it [파드명] -- [명령어] - 특정 파드 내에서 명령어를 실행합니다.",
                            "kubectl get deployment - 현재 네임스페이스의 모든 디플로이먼트를 나열합니다.",
                            "kubectl scale deployment [디플로이먼트명] --replicas=[숫자] - 디플로이먼트의 레플리카 수를 조정합니다.",
                            "kubectl rollout status deployment/[디플로이먼트명] - 디플로이먼트의 롤아웃 상태를 확인합니다.",
                            "kubectl set image deployment/[디플로이먼트명] [컨테이너명]=[이미지]:[태그] - 디플로이먼트의 이미지를 업데이트합니다.",
                            "kubectl get namespace - 모든 네임스페이스를 나열합니다.",
                            "kubectl config view - kubectl의 현재 설정을 보여줍니다.",
                            "kubectl create namespace [네임스페이스명] - 새 네임스페이스를 생성합니다.",
                            "kubectl port-forward [파드명] [로컬포트]:[파드포트] - 파드의 포트를 로컬로 포워딩합니다.",
                            "kubectl get events - 현재 네임스페이스의 이벤트를 나열합니다.",
                            "kubectl attach [파드명] -i - 실행 중인 컨테이너에 연결합니다.",
                            "kubectl run [이름] --image=[이미지] - 새로운 파드를 생성하여 지정된 이미지를 실행합니다.",
                            "kubectl delete -f [파일명] - 구성 파일을 사용하여 리소스를 삭제합니다."
                        ]
                    ])
                ]),
                className="mt-2"
            ),
            width=6
        ),

        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Ul([
                        html.Li(f"{command}") for command in [
                            "po - Pods",
                            "rs - ReplicaSets",
                            "deploy - Deployments",
                            "svc - Services",
                            "ns - Namespaces",
                            "ing - Ingresses",
                            "sc - StorageClasses",
                            "pvc - PersistentVolumeClaims",
                            "pv - PersistentVolumes",
                            "sa - ServiceAccounts",
                            "cm - ConfigMaps",
                            "sec - Secrets",
                            "no - Nodes",
                            "hpa - HorizontalPodAutoscalers",
                            "job - Jobs",
                            "cronjob - CronJobs",
                            "crd - CustomResourceDefinitions"
                        ]
                    ])
                ]),
                className="mt-2"
            ),
            width=6
        ),

    ]),


    # title : K8s 명령어 도우미
    html.H2('K8s 명령어 도우미', style={
        'backgroundColor': 'green',  # The button color from your image
        'color': 'white',  # Text color
        'borderRadius': '20px',  # Rounded corners
        'textAlign': 'center',  # Centered text
        'padding': '10px',  # Padding inside the box
        'fontSize': '1.5rem',  # Font size
        'fontFamily': 'sans-serif',  # Font family
        'fontWeight': 'bold',  # Bold text
        'display': 'inline-block',  # Necessary for padding and border-radius to take effect
        'marginTop': '1rem',  # Top margin
        'marginBottom': '1rem',  # Bottom margin
        'width': '100%'  # Full width
    }),

    # sidebar
    html.Div([

        html.H4('명령어 그룹', style={'textAlign': 'left'}),
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
        'height': '300vh',  # Full height of the viewport
        'box-shadow': '2px 0px 5px 0px rgba(0,0,0,0.1)'  # Adding some shadow for depth
    }),

    # Main content area

    html.Div([
        html.H4('명령어 상세'),
        dcc.Dropdown(id='command-dropdown', style={'marginBottom': '1rem'},),
        html.Div(['Description: ']),
        html.Div(id='command-description'),
        html.Div(['Help Result: ']),
        html.Div(id='help-result')
    ], style={
        'width': '70%',
        'float': 'left',
        'display': 'inline-block',
        'padding': '20px'
    }),
    # At the end of your layout, add this line:
    html.Div(id='dummy-div', style={'display': 'none'}),

], fluid=True)

# Clientside callback for reloading the page
app.clientside_callback(
    """
    function(n_clicks) {
        if(n_clicks > 0) {
            window.location.reload();
        }
    }
    """,
    Output('dummy-div', 'children'),
    Input('reset-button', 'n_clicks'),
)

# Add your callbacks here
@app.callback(
    Output('user-command-result', 'children'),
    [Input('execute-button', 'n_clicks'),
     Input('user-command-input', 'n_submit'),
     Input('get-nodes-button', 'n_clicks'),  # 'get-nodes-button' 입력 추가
     Input('get-svc-button', 'n_clicks'),    # 'get-svc-button' 입력 추가
     Input('get-ns-button', 'n_clicks'),     # 'get-ns-button' 입력 추가
    ],
    [State('user-command-input', 'value')],
        prevent_initial_call=True
)
def execute_command(execute_clicks, input_submit, get_nodes_clicks, get_svc_clicks, get_ns_clicks, command):
    ctx = dash.callback_context

    if not ctx.triggered:
        return None

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'execute-button' or trigger_id == 'user-command-input':
        if command:  # 사용자 입력이 있는지 확인
            output = run_kubectl_command(command)
        else:
            return dcc.Markdown(
                "kubectl 명령어 입력 후 실행해주세요!!!",
                style={'color': 'red'}
            )
    elif trigger_id == 'get-nodes-button':
        output = run_kubectl_command('kubectl get nodes')  # 'kubectl get nodes' 명령 실행
    elif trigger_id == 'get-svc-button':
        output = run_kubectl_command('kubectl get svc -A')  # 'kubectl get svc -A' 명령 실행
    elif trigger_id == 'get-ns-button':
        output = run_kubectl_command('kubectl get ns')  # 'kubectl get ns' 명령 실행
    else:
        return None

    return dcc.Markdown(
        f'```\n{output}\n```',
        style={'white-space': 'pre-wrap', 'background-color': 'black', 'color': 'white', 'padding': '10px'}
    )



@app.callback(
    Output('command-dropdown', 'options'),
    Input('command-group-dropdown', 'value')
)
def update_command_dropdown(selected_group):
    group_commands = commands[selected_group]
    return [{'label': cmd, 'value': cmd} for cmd in group_commands]

@app.callback(
    Output('command-description', 'children'),
    Input('command-dropdown', 'value'),
    State('command-group-dropdown', 'value')
)
def update_command_description(selected_command, selected_group):
    if selected_command:
        description = commands[selected_group][selected_command]
        return html.P(description)

@app.callback(
    Output('help-result', 'children'),
    Input('command-dropdown', 'value'),
    prevent_initial_call=True  # 초기 호출 방지
)
def execute_help_command(selected_command):
    if selected_command:
        output = run_kubectl_command(f'kubectl {selected_command} --help')
        # Use Markdown code block to preserve formatting
        return dcc.Markdown(f'```\n{output}\n```', style={'white-space': 'pre'})


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8050')
