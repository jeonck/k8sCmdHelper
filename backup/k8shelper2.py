import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import subprocess

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def run_kubectl_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        output = stdout.decode('utf-8')
    else:
        output = stderr.decode('utf-8')

    return output.strip()

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H3('kubectl 명령어 실행기', className="bg-primary text-white text-center p-2"),
            width=12
        )
    ),

    dbc.Row([
        dbc.Col(
            dbc.Input(id='user-command-input', type='text', placeholder='kubectl 명령어를 입력하세요.', className="mb-2"),
            width=8
        ),
        dbc.Col([
            dbc.Button('명령어 실행', id='execute-button', color='primary', className="mb-2 me-2"),  # marginRight 추가
            dbc.Button('초기화', id='reset-button', color='secondary', className="mb-2 me-2"),  # marginBottom 유지
        ], width=3, className="d-flex align-items-center")  # 버튼을 같은 열에 넣고 가로로 배치
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Loading(
                id="loading-query-nodes",
                children=[
                    dbc.Button("노드 조회 (kubectl get nodes)", id='query-nodes-button', color='info', className="w-100 mb-2")
                ],
                type="default"
            ),
            width=1
        )
    ]),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Markdown(id='user-command-result', className="text-light bg-dark p-2")
                ]),
                className="mt-2"
            ),
            width=12
        )
    ]),

    dbc.Row([
        dbc.Col(
            html.H4("Top 20 kubectl 명령어", className="text-center mt-4"),
            width=12
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
            width=12
        )
    ])
], fluid=True)

@app.callback(
    Output('user-command-result', 'children'),
    [Input('execute-button', 'n_clicks'), Input('query-nodes-button', 'n_clicks')],
    [State('user-command-input', 'value')],
    prevent_initial_call=True
)
def execute_command(execute_clicks, query_nodes_clicks, command):
    ctx = dash.callback_context

    if not ctx.triggered:
        return None

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'execute-button' and command:
        output = run_kubectl_command(command)
    elif trigger_id == 'query-nodes-button':
        output = run_kubectl_command('kubectl get nodes')
    else:
        output = "명령어를 입력하거나 버튼을 클릭해주세요."

    return f'```\n{output}\n```'

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8051')
