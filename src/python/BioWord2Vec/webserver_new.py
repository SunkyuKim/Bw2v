from flask import Flask, request, render_template, jsonify, send_file
from socket import *
import pygal
import json

app = Flask(__name__)

HOST = 'localhost'
PORT = 21567
BUFSIZ = 4096
ADDR = (HOST, PORT)

def recv_all(the_socket):
    total_data=[]
    while True:
        data = the_socket.recv(BUFSIZ)
        if not data: break
        total_data.append(data)
    return ''.join(total_data)

def get_query():
    pos_text = request.args.get('pos_text')
    neg_text = request.args.get('neg_text')
    topn = int(request.args.get('top_n'))
    pos_words = [q.strip().replace(" ", "_") for q in pos_text.split('\n') if len(q.strip()) > 0]
    neg_words = [q.strip().replace(" ", "_") for q in neg_text.split('\n') if len(q.strip()) > 0]
    return pos_words, neg_words, topn

def get_data_from_server(server_request):
    tcpCliSocket = socket(AF_INET, SOCK_STREAM)
    tcpCliSocket.connect(ADDR)

    tcpCliSocket.sendall(json.dumps(server_request))
#    vec_str = tcpCliSocket.recv(BUFSIZ)
    vec_str = recv_all(tcpCliSocket)
    tcpCliSocket.close()

    return vec_str

@app.route('/')
def index():
    # return "a<br>b"
    return render_template('index.html')

@app.route('/buru')
def index_page():
    return render_template('index_buru.html',parm=True)

@app.route('/demo')
def demo_page():
    return render_template('demo_buru.html',parm=False)

@app.route('/2')
def index2():
    # return "a<br>b"
    return render_template('page.html')

@app.route('/htmls/<html_file_name>')
def renderer(html_file_name):
    return render_template(str(html_file_name))

@app.route('/download/temp_files/<file_name>')
def download(file_name):
    return send_file('templates/temp_files/' + str(file_name))

@app.route('/download/releases/<file_code>')
def release(file_code):
    if file_code == 'bin_100':
        return send_file('res/100dim_160526.bin')
    elif file_code == 'bin_300':
        return send_file('res/300dim_160629.bin')
    elif file_code == 'text_100':
        return send_file('res/bulk_100d.zip')
    elif file_code == 'text_300':
        return send_file('res/bulk_300d.zip')
# @app.route('/nearest.svg')
def return_chart(reduced_data):
    vis_dict = dict()

    for point in reduced_data:
        if point['type'] not in vis_dict.keys():
            vis_dict[point['type']] = list()

        vis_dict[point['type']].append({'value':(point['x'], point['y']), 'label':point['term'],
                              'xlink':"http://best.korea.ac.kr/s?otype=&q=%s&t=l&wt=xslt&tr=l.xsl"%point['term']})

    scatter_chart = pygal.XY(show_x_guides=True, stroke=False, print_labels=False, dots_size=3)

    for type in vis_dict.keys():
        scatter_chart.add(type, vis_dict[type])

    chart = scatter_chart.render_data_uri()

    return render_template('scatter_chart.html', chart=chart)

    # return scatter_chart.render_response()
@app.route('/result/file')
def result_file():
    pos_words, neg_words, topn = get_query()

    server_query = {
        'command':'get',
        'topn':topn,
        'pos_query':pos_words,
        'neg_query':neg_words
    }

    server_result_jsonstr = get_data_from_server(server_query)
    print "good!"
    server_result = json.loads(server_result_jsonstr)
    
    print server_result 
    vec = server_result['filepath']
    # if server_result['reduced_data'] == 'null':
    #     chart = None
    # else:
    #     chart = return_chart(server_result['reduced_data'])

    # top10terms = server_result['terms'][0:9]
    top10terms = server_result['terms']
    return jsonify(
        terms='<br>'.join(top10terms),
        vec=vec,
        # chart=chart
    )

@app.route('/result/xy')
def result_xy():
    filepath = request.args.get('filepath').split('/')[-1]
    server_query = {
        'command': 'get_xy',
        'filepath': 'templates/temp_files/' + filepath
    }
    server_result_jsonstr = get_data_from_server(server_query)
    server_result = json.loads(server_result_jsonstr)

    if server_result['reduced_data'] == 'null':
        chart = None
    else:
        chart = return_chart(server_result['reduced_data'])
    return jsonify(
        chart=chart
    )

@app.route('/sim_result')
def get_similarity():
    termA = request.args.get('termA').strip().replace(" ", "_")
    termB = request.args.get('termB').strip().replace(" ", "_")
    server_query = {
        'command':'get_similarity',
        'termA':termA,
        'termB':termB
    }
    server_result_jsonstr = get_data_from_server(server_query)
    server_result = json.loads(server_result_jsonstr)
    if server_result['similarity'] == 'null':
        return jsonify(
            similarity='Invalid query'
        )
    return jsonify(similarity=server_result["similarity"])

if __name__ == '__main__':
    app.run(debug=True)
