from django.shortcuts import render

def dashboard(request):
    # data = {
    #     "money_today": "$53K",
    #     "users_today": "2,300",
    #     "new_clients": "3,462",
    #     "sales": "$103,430",
    #     "website_views": [20, 40, 30, 50, 60, 70, 50],  # Example data
    #     "daily_sales": [300, 400, 500, 600, 450, 700],  # Example data
    #     "completed_tasks": [400, 450, 500, 550, 600, 650],  # Example data
    # }
    return render(request, "dashboard/dashboard.html")