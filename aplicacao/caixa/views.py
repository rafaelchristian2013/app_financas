from django.shortcuts import render, redirect, get_object_or_404
from caixa.models import Transacao
# from datetime import datetime, timedelta
import datetime
import calendar

def index(request):
    # Data
    today = datetime.date.today()
    today1 = datetime.datetime.today()
    print("tipo: {} valor:{}".format(type(today1), today1))
    # today1 = datetime.datetime.strptime(str(today1), '%Y-%m-%d')

    today_month = today.strftime("%m")
    today_year = today.strftime("%Y")
    my_month = today.strftime("%b")
    today = today.strftime("%Y%m%d")
    ###
    last_day = calendar.monthrange(today1.year, today1.month)[1]
    last_complete = today1.replace(day=last_day)
    print('ultimo desse mes{}'.format(last_complete))

    transacoes = Transacao.objects.order_by('-data_transacao').filter(data_transacao__year=today_year, data_transacao__month=today_month)  

    despesas = Transacao.objects.order_by('-data_transacao').filter(tipo_transacao='saida').filter(data_transacao__lte = last_complete)

    entradas = Transacao.objects.order_by('-data_transacao').filter(tipo_transacao='entrada').filter(data_transacao__lte = last_complete)
    total_despesas = 0
    
    for despesa in despesas:
        total_despesas += despesa.valor_transacao


    total_entradas = 0
    for entrada in entradas:
        total_entradas += entrada.valor_transacao

    total_em_caixa = total_entradas - total_despesas 
    # total_em_caixa = "{:.02f}".format(total_em_caixa)
    dados = {
        'despesas' : total_despesas,
        'entradas' : total_entradas,
        'em_caixa' : total_em_caixa,
        'transacoes': transacoes,
        'data_hoje': today,
        'mes' : my_month,
        'ano': today_year
    }

    

    print(today)
    return render(request, 'index.html', dados)

def previous(request, dataprevious):
    print("data {}" .format(dataprevious))
    dataprevious = datetime.datetime.strptime(str(dataprevious), '%Y%m%d')
    first = dataprevious.replace(day=1)
    print("data depois {}" .format(dataprevious))
    prev_date = first - datetime.timedelta(days=1)
    prev_date_1 = prev_date
    my_month = prev_date.strftime("%b")
    previous_year = prev_date.year
    previous_month= prev_date.month
    prev_date = prev_date.strftime("%Y%m%d")

    last_day = calendar.monthrange(previous_year, previous_month)[1]
    print("tipo: {} valor:{}".format(type(prev_date_1), prev_date_1))
    last_complete = prev_date_1.replace(day=last_day)

    transacoes = Transacao.objects.order_by('-data_transacao').filter(data_transacao__year=previous_year, data_transacao__month=previous_month)                                                                
    despesas = Transacao.objects.order_by('-data_transacao').filter(tipo_transacao='saida').filter(data_transacao__lte = last_complete)
    entradas = Transacao.objects.order_by('-data_transacao').filter(tipo_transacao='entrada').filter(data_transacao__lte = last_complete)

    total_despesas = 0
    for despesa in despesas:
        total_despesas += despesa.valor_transacao


    total_entradas = 0
    for entrada in entradas:
        total_entradas += entrada.valor_transacao

    total_em_caixa = total_entradas - total_despesas 
    # total_em_caixa = "{:.02f}".format(total_em_caixa)
    dados = {
        'despesas' : total_despesas,
        'entradas' : total_entradas,
        'em_caixa' : total_em_caixa,
        'transacoes': transacoes,
        'data_pag': prev_date,
        'mes' : my_month,
        'ano': previous_year
        
    }

    

    print(prev_date)
    return render(request, 'previous.html', dados)

def next(request, datanext):
    # print("data {}" .format(datanext))
    datanext = datetime.datetime.strptime(str(datanext), '%Y%m%d')
    last = datanext.replace(day=28) + datetime.timedelta(days=4)
    # print("data depois {}" .format(datanext))
    next_date = last + datetime.timedelta(days=1)
    next_date1 = next_date
    my_month = next_date.strftime("%b")
    next_year = next_date.year
    next_month= next_date.month
    next_date = next_date.strftime("%Y%m%d")

    last_day = calendar.monthrange(next_year, next_month)[1]
    last_complete = next_date1.replace(day=last_day)

    print("next_date {}" .format(next_date))
    transacoes = Transacao.objects.order_by('-data_transacao').filter(data_transacao__year=next_year, data_transacao__month=next_month)                                                                           
    despesas = Transacao.objects.order_by('-data_transacao').filter(tipo_transacao='saida').filter(tipo_transacao='entrada').filter(data_transacao__lte = last_complete)
    entradas = Transacao.objects.order_by('-data_transacao').filter(tipo_transacao='entrada').filter(tipo_transacao='entrada').filter(data_transacao__lte = last_complete)

    total_despesas = 0
    for despesa in despesas:
        total_despesas += despesa.valor_transacao


    total_entradas = 0
    for entrada in entradas:
        total_entradas += entrada.valor_transacao

    total_em_caixa = total_entradas - total_despesas 
    # total_em_caixa = "{:.02f}".format(total_em_caixa)
    dados = {
        'despesas' : total_despesas,
        'entradas' : total_entradas,
        'em_caixa' : total_em_caixa,
        'transacoes': transacoes,
        'data_pag': next_date,
        'mes' : my_month,
        'ano':next_year

    }

    

    print(next_date)
    return render(request, 'next.html', dados)

def nova(request):
    if request.method == 'POST':
        nome_transacao = request.POST['description'] 
        if nome_transacao == '':
            print('Descreva a transação')
            return redirect('nova')  
        valor_transacao = request.POST['amount']
        if valor_transacao == '':
            print('Defina o valor da transação')
            return redirect('nova')  
        tipo_transacao = request.POST.get('opcao', False)
        if tipo_transacao == False:
            print('Escolha um tipo')
            return redirect('nova')  
        date_transacao = request.POST['date'] 
        if date_transacao == '':
            print('Escolha a data')
            return redirect('nova')
        print(date_transacao)
        
        tran = Transacao.objects.create(nome_transacao=nome_transacao, valor_transacao=valor_transacao, data_transacao=date_transacao, tipo_transacao=tipo_transacao)
        tran.save()
        return redirect('index')
    return render(request, 'formulario.html')

def transacao(request, transacao_id): # transacao_id indica recebimento
    transacao = get_object_or_404(Transacao, pk=transacao_id)
    transacao_a_exibir = {
        'transacao' : transacao
    }
    return render(request,'transacao.html', transacao_a_exibir)

def edita_transacao(request, transacao_id):
    transacao = get_object_or_404(Transacao, pk=transacao_id)
    transacao_a_editar = { 'transacao' : transacao }
    print(transacao.data_transacao)
    return render(request, 'edita_transacao.html', transacao_a_editar)

def atualiza_transacao(request):
    if request.method == 'POST':
        transacao_id = request.POST['transacao_id']
        t = Transacao.objects.get(pk=transacao_id)
        t.nome_transacao = request.POST['description']
        t.valor_transacao = request.POST['amount']
        t.data_transacao = request.POST['date']
        t.tipo_transacao = request.POST['opcao']
        t.save()
        return redirect('index')

def deleta_transacao(request, transacao_id):
    transacao = get_object_or_404(Transacao, pk=transacao_id)
    transacao.delete()
    return redirect('index')

# def pagina_anterior(request):
#     transacoes = Transacao.objects.filter(data_transacao__year=2020,
#                                          data_transacao__month=11)
#     despesas = Transacao.objects.filter(data_transacao__year=2020,
#                                          data_transacao__month=11).filter(tipo_transacao='saida') 
#     entradas = Transacao.objects.filter(data_transacao__year=2020,
#                                          data_transacao__month=11).filter(tipo_transacao='entrada')     
# def proxima_pagina(request):
#     transacoes = Transacao.objects.filter(data_transacao__year=2020,
#                                          data_transacao__month=11)
#     despesas = Transacao.objects.filter(data_transacao__year=2020,
#                                          data_transacao__month=11).filter(tipo_transacao='saida') 
#     entradas = Transacao.objects.filter(data_transacao__year=2020,
#                                          data_transacao__month=11).filter(tipo_transacao='entrada') 
#  import datetime
#  today = datetime.date.today()
#  first = today.replace(day=1)
#  lastMonth = first - datetime.timedelta(days=1)
#  print(lastMonth.strftime("%Y%m"))  