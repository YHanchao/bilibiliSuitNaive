from time import strftime, localtime
errors = {
    0: 'Input Error! Cannot find certain suit.',
    1: 'Network Error! Cannot get certain resource.',
    2: 'File Error! Cannot save certain resource.',
    3: 'Invalid Query! Cannot run certain query.',
    4: 'Invalid File Name! Files contains invalid argument.',
    5: 'File Error! Cannot open certain resource.',
    6: 'Other Errors!',
    101: 'Success with Error'
}


def _show_error(error_id):
    print(strftime('%Y-%m-%d %H:%M:%S', localtime()) + ': ' + errors[error_id])
    with open('error_log', 'a', encoding='utf-8') as error_log:
        error_log.write(strftime('%Y-%m-%d %H:%M:%S', localtime()) + ': ' + errors[error_id] + '\n')
    return error_id
