from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView
from .models import area, ordenes_pago, concepto
from appOpago.forms import AreaForm, OPForm, conceptoForm, respuestaForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

# Create your views here.
class seccionOP(LoginRequiredMixin, View):
    def get(self, request):
        areas = area.objects.all()
        contexto = {'areas' : areas}
        return render (request, 'opago/home.html', contexto)

def listarArea(request,):
    areas = area.objects.all()
    contexto = {'areas' : areas}
    return render (request, 'opago/listar_area.html', contexto)

def crearArea (request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Registro Guardado')
            return redirect('listar_area')
    else:
        form = AreaForm()
    return render(request, 'opago/crear_area.html', {'form' : form})

def editarArea(request,id):
    areas = area.objects.get(id=id)
    if request.method == 'GET':
        form = AreaForm(instance=areas)
    else:
        form=AreaForm(request.POST, instance=areas)
        if form.is_valid():
            form.save()
            return redirect ('listar_area')
    return render (request, 'opago/editar_area.html', {'form' : form})

def eliminarArea(request,id):
    areas = area.objects.get(id=id)
    if request.method == 'POST':
        areas.delete()
        return redirect ('listar_area')
    return render (request, 'opago/eliminar_area.html', {'areas' : areas})
    
class listOrden(ListView):
    model = ordenes_pago
    template_name = 'opago/consulta_area.html'

    # def get_queryset(self):
    #     if self.request.user.groups.filter(name='areas'):
    #         queryset = ordenes_pago.filter(area = self.request.user.area)
    #         return queryset
    #     else:
    #         queryset = ordenes_pago.objects.all()
    #         return queryset

class createOrden(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    model = ordenes_pago
    form_class = OPForm
    template_name = 'opago/nueva_orden.html'
    success_url = reverse_lazy('consulta_area')

class ticket(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template = get_template('opago/ticket.html')
        context = {
            'ordenes_pago': ordenes_pago.objects.get(pk=self.kwargs['pk']),
            'comp': {'name': 'H. Ayuntamiento de Tzompantepec', 'ruc': '2414152315', 'address': 'Centro, 90490 Tzompantepec, Tlax.', 'titulo': 'Ticket de pago'},
        }
        html = template.render(context)
        response = HttpResponse(content_type='aplication/pdf')
        response['content-Disposition'] = 'attachment; filename="Ticket.pdf"'
        pisa_status = pisa.CreatePDF(
            html, dest=response
        )
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some error <pre>' + html + '</pre>')
        return response
    
    def list_history(request):
        orden = ordenes_pago.objects.all()
        contexto = {'orden' : orden}
        return render (request, 'opago/reportes.html', contexto)
    
def listarConcepto(request):
    conceptos = concepto.objects.all()
    contexto = {'conceptos' : conceptos}
    return render (request, 'opago/listar_concepto.html', contexto)

def crearConcepto (request):
    if request.method == 'POST':
        form = conceptoForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, '¡Concepto Registrado')
            return redirect('listar_conceptos')
    else:
        form = conceptoForm()
    return render(request, 'opago/crear_concepto.html', {'form':form})

def editarConcepto(request,id):
    conceptos = concepto.objects.get(id=id)
    if request.method == 'GET':
        form = conceptoForm(instance=conceptos)
    else:
        form=conceptoForm(request.POST, instance=conceptos)
        if form.is_valid():
            form.save()
            return redirect ('listar_conceptos')
    return render (request, 'opago/editar_concepto.html', {'form' : form})

def eliminarConcepto(request,id):
    conceptos = concepto.objects.get(id=id)
    if request.method == 'POST':
        conceptos.delete()
        return redirect ('listar_conceptos')
    return render (request, 'opago/eliminar_concepto.html', {'conceptos' : conceptos})

def reportes(request):
    orden = ordenes_pago.objects.all()
    contexto = {'orden' : orden}
    return render (request, 'opago/reportes.html', contexto)

class estatus (LoginRequiredMixin, ListView):
    model = ordenes_pago
    template_name = 'opago/caja.html'

class updateEstatus (LoginRequiredMixin, UpdateView):
    model = ordenes_pago
    form_class = respuestaForm
    template_name = 'opago/modificar.html'
    success_url = reverse_lazy('caja')

class pdfView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template = get_template('opago/comprobante.html')
        context = {
            'ordenes_pago': ordenes_pago.objects.get(pk=self.kwargs['pk']),
            'comp': {'name': 'H. Ayuntamiento de Tzompantepec', 'ruc': '2414152315',
                     'address': 'Centro, 90490 Tzompantepec, Tlax.'},
        }
        html = template.render(context)
        response = HttpResponse(content_type='aplication/pdf')
        response['content-Disposition'] = 'attachmente; filename="comprobante.pdf"'
        pisa_status = pisa.CreatePDF(
            html, dest=response
        )
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('we had some errors <pre>' + html + '</pre>')
        return response