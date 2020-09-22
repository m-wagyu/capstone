def alert_build(alert:dict):
  try:
    ts = alert['timestamp'].split('T')
    date = ts[0]
    time = ts[1].split('.')[0]

    if 'src_port' in alert.keys():
      src = "{}:{}".format(alert['src_ip'],alert['src_port'])
    else:
      src = alert['src_ip']
    if 'dest_port' in alert.keys():
      dst = "{}:{}".format(alert['dest_ip'],alert['dest_port'])
    else:
      dst = alert['dest_ip']
  except KeyError:
    return None

  return {'time':'{} {}'.format(date,time),
        'src_dst':'{} -> {}'.format(src,dst),
        'proto':alert['proto'],
        'action':alert['alert']['action'],
        'message':alert['alert']['signature']}
