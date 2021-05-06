from flask import Blueprint, request

from manager import db
from manager.models import Dataflow

dataflow_service = Blueprint('dataflow_service', __name__)


@dataflow_service.route('/dataflow', methods=['GET', 'POST', 'DELETE'])
def dataflow():
    if request.method == 'POST':
        return create_dataflow(request.form.get('source_url'), request.form.get('protocol'),
                               request.form.get('app_name'), request.args.get('id'))

    elif request.method == 'GET':
        return get_dataflow(request.args.get('protocol'), request.args.get('app_name'))

    else:
        return delete_dataflow(request.args.get('id'))


def create_dataflow(source_url: str, protocol: int, app_name: str, dataflow_id: str):
    if source_url and protocol and app_name and dataflow_id:
        data = Dataflow.query.filter_by(dataflow_id=dataflow_id).first()
        if data:
            data.source_url, data.protocol, data.app_name = source_url, protocol, app_name
        else:
            data = Dataflow(source_url=source_url, protocol=protocol, app_name=app_name, dataflow_id=dataflow_id)
            db.session.add(data)
        db.session.commit()
        return {
            'status': True,
            'msg': f'dataflow {source_url} registered successfully'
        }

    else:
        return {
            'status': False,
            'msg': 'Please provide source_url, protocol, app_name, and dataflow_id'
        }


def get_dataflow(protocol: int, app_name: str):
    if protocol and app_name:
        data = Dataflow.query.filter_by(protocol=protocol, app_name=app_name).first()
        if data:
            return {
                'status': True,
                'source_url': data.source_url
            }
        else:
            return {
                'status': False,
                'msg': "dataflow for the app doesn't exist"
            }
    return {
        'status': False,
        'msg': 'Please provide both protocol and app_name'
    }


def delete_dataflow(dataflow_id: str):
    data = Dataflow.query.filter_by(dataflow_id=dataflow_id).first()
    if data:
        db.session.delete(data)
        db.session.commit()
        return {
            'status': True,
            'msg': "dataflow has been deleted"
        }
    return {
        'status': True,
        'msg': "dataflow doesn't exist"
    }