from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Create your views here.
def home(request):
  import requests
  import json

  if request.method == 'POST':
    ticker = request.POST['ticker']

    # pk_79bd4f172253407d985e42b18d842953
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/batch?types=quote,news,chart&range=1m&last=10&token=pk_79bd4f172253407d985e42b18d842953")

    try:
      api = json.loads(api_request.content)
    except Exception as e:
      api = "Error..."
    
    return render(request, 'home.html', {'api': api})

  else:
    messages.success(request, ("Error. There was a problem with your ticker symbol. Please try again."))
    return render(request, 'home.html', {'ticker': ''})



def about(request):
  return render(request, 'about.html', {})



def add_stock(request):
  import requests
  import json

  if request.method == 'POST':
    form = StockForm(request.POST or None)

    if form.is_valid():
      form.save()
      messages.success(request, ("Stock has been added."))
      return redirect('add_stock')

  else:
    ticker = Stock.objects.all()
    output = []

    for ticker_item in ticker:
      api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) +"/batch?types=quote,news,chart&range=1m&last=10&token=pk_79bd4f172253407d985e42b18d842953")
      try:
        api = json.loads(api_request.content)
        output.append(api)
      except Exception as e:
        api = "Error..."


    return render(request, 'add_stock.html', {'ticker': ticker, 'output' : output})




def delete(request, stock_id):
  item = Stock.objects.get(pk=stock_id)
  item.delete()
  messages.success(request, ("Stock has been deleted"))
  return redirect(add_stock)