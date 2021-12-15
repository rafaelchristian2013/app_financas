from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:transacao_id>', views.transacao, name='transacao'), #indica recebimento de id enviado pelo href
    path('edita/<int:transacao_id>', views.edita_transacao, name='edita_transacao'), 
    path('deleta/<int:transacao_id>', views.deleta_transacao, name='deleta_transacao'), 
    path('previous/<int:dataprevious>', views.previous, name='previous'), 
    path('next/<int:datanext>', views.next, name='next'), 
    path('atualiza_transacao', views.atualiza_transacao, name='atualiza_transacao'), 
    path('novatrasacao', views.nova, name='nova')
]