print('my_requisitions')
is_filter = True

if len(filter_my_requisitions) > 1:
    filter_my_requisitions_value = True

if user_id.department_head:
    filter_domain.append('|')
    filter_domain.append('|')
    filter_domain.append('|')
    filter_domain.append('|')
    filter_domain.append(('app_state', '=', ''))
    filter_domain.append(('app_state', '=', 'draft'))
    filter_domain.append(('app_state', '=', None))
    filter_domain.append(('department_head_state', '=', 'accepted'))
    filter_domain.append(('department_head_state', '=', 'canceled'))

if user_id.it_department:
    filter_domain.append(('req_from', '=', 'it'))
    filter_domain.append(('app_state', '=', 'approve_dh'))

if user_id.admin_department:
    filter_domain.append('|')
    filter_domain.append(('app_state', '=', 'approve_dh'))
    filter_domain.append(('app_state', '=', 'approve_it'))

if user_id.finance_department:
    filter_domain.append(('app_state', '=', 'approve_admin'))

if user_id.scm_department:
    filter_domain.append(('app_state', '=', 'approve_finance'))