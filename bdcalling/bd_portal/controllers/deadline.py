# def date_diff_in_seconds(dt2, dt1):
#     timedelta = dt1 - dt2
#     return timedelta.days * 24 * 3600 + timedelta.seconds
#
# def dhms_from_seconds(seconds):
#     minutes, seconds = divmod(seconds, 60)
#     hours, minutes = divmod(minutes, 60)
#     days, hours = divmod(hours, 24)
#     return (days, hours, minutes, seconds)
#
# for sale in sales:
#
#     # date1 = datetime.strptime('2024-04-16 01:00:00', '%Y-%m-%d %H:%M:%S')  # Original
#     # date1 = datetime.strptime('2024-04-20', '%Y-%m-%d')
#     delivery_last_date = sale.delivery_last_date
#     date1 = datetime.combine(delivery_last_date, datetime.min.time())
#     print('date1', date1)
#     date2 = datetime.now()
#
#     elapsed = dhms_from_seconds(date_diff_in_seconds(date2, date1))
#     if elapsed[0] < 0 or elapsed[3] < 0:
#         sale.deadline = 'Late Delivery'
#     else:
#         deadline = "%d D, %d H, %d M, %d S" % dhms_from_seconds(date_diff_in_seconds(date2, date1))
#         sale.deadline = deadline