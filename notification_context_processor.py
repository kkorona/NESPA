def notification(request):
	context = {
		'notification_list' : ["테스트입니다1", "테스트입니다2"],
	}

	return context
