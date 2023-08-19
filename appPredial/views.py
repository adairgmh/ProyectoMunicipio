from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse

from appPredial.models import Predio, Contribuyente, Pago
from appPredial.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin
from appPredial.forms import *
from pprint import pprint
from datetime import datetime
import requests

import json

def contribuyentePago(request):
    
    #Buscar en base a la clave catastral
    pago_obj = {}
    predio= None
    query = None
    try:
        query = request.GET.get("buscar")   
             
    except ValueError:
        print('Invalid Value')
    
    try:
        
        pago_obj = Pago.objects.filter(claveCatastral=query).order_by('agnio')
        
    except ValueError:
        messages.error(request, 'Has ingresado un valor invalido')
        
    try:
        predio = Predio.objects.filter(claveCatastral=query)
        
    except ValueError:
        messages.error(request, 'Has ingresado un valor invalido')

    


    context={
        "object_list" : pago_obj,
        "query" : query,
        "predio": predio,
        
    }

    return render(request, 'contribuyente/contribuyentePago.html', context=context)

class contribuyentePagoCreateView(CreateView):
    
    form_class = contribuyentepagoForm
    model = Pago
    template_name = 'contribuyente/contribuyentePago_add.html'
    success_url =  reverse_lazy('predial:historial_pagados')
    

    def get(self, request, **kwargs):
        query = request.GET.get("query")
        predio = Predio.objects.get(claveCatastral=query)
        
        field_name = 'idtipo'
        temp = Predio.objects.get(claveCatastral=query)
        field_object = Predio._meta.get_field(field_name)
        field_value = field_object.value_from_object(temp)
        
        field_name2 = 'costo'
        temp2 = TipoPredio.objects.get(id=field_value)
        field_object2 = TipoPredio._meta.get_field(field_name2)
        field_value2 = field_object2.value_from_object(temp2)
        
        costoPredio=field_value2
        
        fechaPago = datetime.today().strftime('%d/%m/%Y')
        
        recargo = self.calcularRecargo(tasabase=costoPredio)
        descuento = 1
        
        total = costoPredio + recargo
        
        form = contribuyentepagoForm(claveCatastral=predio, 
                                     monto=costoPredio, 
                                     fecha=fechaPago, 
                                     recargo=recargo,
                                     total=total,
                                     )
        
        context={
            "form": form,
            "title" : 'Pagar',
            "entity" : 'Pagos',
            "action": 'add',
            "tasabase": costoPredio,
            "list_url": reverse_lazy('predial:contribuyente_historial'),
            "claveCatastral": query,
            "recargo": recargo,
            "descuento": descuento,
            "fechaPago": fechaPago,
            "total": total,
        
        }

        return render(request, self.template_name, context=context, )

    def calcularRecargo(request, tasabase):
        try: 
            field_name = 'agnio'
            recargo = 0.0
            temp = Pago.objects.all().last()
            
            if temp is not None:
                field_object = Pago._meta.get_field(field_name)
                field_value = field_object.value_from_object(temp)
                ultimoAgnioPagado = field_value
                
                if ultimoAgnioPagado == int(datetime.today().strftime('%Y')):
                    return recargo
                else: 
                    mesActual = int(datetime.today().strftime('%m'))
                    recargo = (0.05 * tasabase)*(mesActual-1)
                    return recargo
            else:
                return recargo
            
        except ObjectDoesNotExist:
            messages.error(request, 'No existe ese Pago')
            return render(request, "personal/pago/historial_pagados.html")
        
        
    
    def post(self, request, *args, **kwargs):
        data = {}
        
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class Predial(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'predial.view_predio','predial.view_contribuyente'
    template_name = 'personal/predial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


""" Vistas de la seccion predios """


def predioBuscar(request):

    #Validacion de Usuario
    user = request.user
    if not user.is_authenticated:
        return redirect('/personal')

    #Buscar en base a la clave catastral
    predio_obj = {}
    contribuyente= None
    query = None
    try:
        query = request.GET.get("buscar")
        if query is not None:
            query = query.upper().strip()
    except ValueError:
        print('Invalid Value')
    
    try:
        
        predio_obj = Predio.objects.filter(rfc=query)
        print(predio_obj)
    except ValueError:
        messages.error(request, 'Has ingresado un valor invalido')
        
    try:
        contribuyente = Contribuyente.objects.filter(rfc=query)
        print(contribuyente)
    except ValueError:
        messages.error(request, 'Has ingresado un valor invalido')

    context={
        "object_list" : predio_obj,
        "query" : query,
        "contribuyente": contribuyente,
        
    }

    return render(request, 'personal/predio/predio_list.html', context=context)

class predioCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):

    permission_required = 'predial.add_predio'
    form_class = predioForm
    model = Predio
    template_name = 'personal/predio/predio_add.html'
    success_url = reverse_lazy('predial:predio_list')

    def get(self, request, **kwargs):
        query = request.GET.get("query")
        contribuyente = Contribuyente.objects.get(rfc=query)
        
        form = predioForm(rfc=contribuyente)
        
        context={
        "form": form,
        "title" : 'Registrar Predio',
        "entity" : 'Predios',
        "action": 'add',
        "comunidades":Comunidad.objects.all(),
        "colonias":Colonia.objects.all(),
        "codigosPostales":CodigoPostal.objects.all(),
        "tiposPredios":TipoPredio.objects.all(),
        
        "list_url": reverse_lazy('predial:predio_list'),
        

        }


        return render(request, self.template_name, context=context)
    
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data) 
        
class predioUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    
    permission_required = 'predial.change_predio'
    form_class = predioForm
    model = Predio
    template_name = 'personal/predio/predio_edit.html'
    success_url = reverse_lazy('predial:predio_list')
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data) 
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Predio'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('predial:predio_list')
        
        return context 

class predioDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    permission_required = 'predial.delete_predio'
    template_name = 'personal/predio/predio_delete.html'
    model = Predio
    success_url = reverse_lazy('predial:predio_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion del predio'
        context['list_url'] = reverse_lazy('predial:predio_list')
        return context 
        

""" Vistas de la seccion Contribuyentes """

class contribuyenteListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'predial.view_contribuyente'
    model = Contribuyente
    template_name = 'personal/contribuyente/contribuyente_list.html'

    """ @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) """
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Contribuyentes'
        context['create_url'] = reverse_lazy('predial:contribuyente_add')
        
        
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = Contribuyente.objects.get(pk = request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data) 

class contribuyenteCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'predial.add_contribuyente'
    form_class = contribuyenteForm
    model = Contribuyente
    template_name = 'personal/contribuyente/contribuyente_add.html'
    success_url = reverse_lazy('predial:contribuyente_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
                
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar un Nuevo Contribuyente'
        context['entity'] = 'Contribuyentes'
        context['action'] = 'add'
        context['estados'] = Estado.objects.all()
        context['municipios'] = Municipio.objects.all()
        context['comunidades'] = Comunidad.objects.all()
        context['colonias'] = Colonia.objects.all()
        context['list_url'] = reverse_lazy('predial:contribuyente_list')
        return context
    
    
    
    
    
class contribuyenteUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'predial.change_contribuyente'
    form_class = contribuyenteForm
    model = Contribuyente
    template_name = 'personal/contribuyente/contribuyente_edit.html'
    success_url = reverse_lazy('predial:contribuyente_list')
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data) 
   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Contribuyente'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('predial:contribuyente_list')
        
        return context 

class contribuyenteDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    
    permission_required = 'predial.delete_contribuyente'
    template_name = 'personal/contribuyente/contribuyente_delete.html'
    model = Contribuyente
    success_url = reverse_lazy('predial:contribuyente_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de Contribuyente'
        context['list_url'] = reverse_lazy('predial:contribuyente_list')
        return context


""" Vistas de la seccion Pagos """

class PagoView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'predial.view_pago'
    template_name = 'personal/pago/pago_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class HistorialAdeudosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'predial.view_pago'
    model = Pago
    template_name = 'personal/pago/historial_adeudos.html'

    """ @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) """
    
    def get(self, request, **kwargs):
        #Creacion del Adeudo automaticamente

        predio_object = Predio.objects.all()
        formaPago = FormaPago.objects.all()
        print("Aqui esta predio_object: ", predio_object)
        
        
        time = datetime.now()
        year = int(time.strftime('%Y'))
        for x in predio_object:
            ultimoPagoRegistrado = Pago.objects.filter(claveCatastral=x).order_by('agnio').last()
            print("Aqui esta ultimoPagoRegistrado", ultimoPagoRegistrado)
            if ultimoPagoRegistrado is None:
                pass
                #messages.error(request, 'No tienes pagos registrados')
            else:
                field_object = Pago._meta.get_field('agnio')
                ultimoAgnioRegistrado = field_object.value_from_object(ultimoPagoRegistrado)
                print("Aqui esta ultimoAgnioRegistrado: ", ultimoAgnioRegistrado)
                if ultimoAgnioRegistrado < year:
                    contador = year - ultimoAgnioRegistrado
                    while contador > 0:
                        ultimoAgnioRegistrado = ultimoAgnioRegistrado + 1
                        Pago.objects.create(claveCatastral=x, fechaPago=date.today(),formaPago=formaPago[0],agnio=ultimoAgnioRegistrado)
                        contador = contador - 1 
                    

                        
                

            
        object_list = Pago.objects.filter(status_pagado = False)
        
       
        
        context={
        "object_list":object_list,
        "entity" : 'Historial de Adeudos',
        "create_url": reverse_lazy('predial:pago_add'),      

        }


        return render(request, self.template_name, context=context)
    
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = Pago.objects.filter(pk = request.POST['id'], status_pagado = False).toJSON().order_by('fechaPago')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
def pago(request):

    #Validacion de Usuario
    user = request.user
    if not user.is_authenticated:
        return redirect('/personal')

    #Buscar en base a la clave catastral
    pago_obj = {}
    predio= None
    query = None
    try:
        query = request.GET.get("buscar")   
        if query is not None:
            query = query.upper().strip()  
             
    except ValueError:
        print('Invalid Value')
    
    try:
        
        pago_obj = Pago.objects.filter(claveCatastral=query).order_by('agnio')
        
    except ValueError:
        messages.error(request, 'Has ingresado un valor invalido')
        
    try:
        predio = Predio.objects.get(claveCatastral=query)
                
    except ObjectDoesNotExist:
            if query != None:
                #messages.error(request, 'No existe ese Predio')
                #return render(request, "personal/pago/historial_pagados.html")
                pass
    context={
        "object_list" : pago_obj,
        "query" : query,
        "predio": predio,
        
    }

    return render(request, 'personal/pago/historial_pagados.html', context=context)

class pagoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'predial.add_pago'
    form_class = pagoForm
    model = Pago
    template_name = 'personal/pago/pago_add.html'
    success_url =  reverse_lazy('predial:historial_pagados')
    
    def get(self, request, **kwargs):
        claveCatastral = self.object.claveCatastral
        print ("a: ",claveCatastral)
        agnio = self.object.agnio
        print ("agnio: ",agnio)
        try: 
            predio = Predio.objects.get(claveCatastral=claveCatastral)
            
        except ObjectDoesNotExist:
            messages.error(request, 'xd')
            return render(request, "personal/pago/historial_pagados.html")
        
        field_name = 'idtipo'
        temp = Predio.objects.get(claveCatastral=claveCatastral)
        field_object = Predio._meta.get_field(field_name)
        field_value = field_object.value_from_object(temp)
        
        field_name2 = 'costo'
        temp2 = TipoPredio.objects.get(id=field_value)
        field_object2 = TipoPredio._meta.get_field(field_name2)
        field_value2 = field_object2.value_from_object(temp2)
        
        costoP=field_value2
        
        #Fecha de Pago
        time = datetime.now()
        date = time.strftime('%d/%m/%Y')
                    
        form = pagoForm(claveCatastral=predio, monto=costoP, fechaPago=date, agnio=agnio)
    
       
        context={
        "form": form,
        "title" : 'Cobrar',
        "entity" : 'Pagos',
        "action": 'edit',
        "query": claveCatastral,
        "tasabase": costoP,
        
        }


        return render(request, self.template_name, context=context)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            
            if action == 'edit':
                form = self.get_form()
                
                data = form.save()
                
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) 
   
class pagoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = 'predial.add_pago'
    form_class = pagoForm
    model = Pago
    template_name = 'personal/pago/pago_add.html'
    
    def get(self, request, **kwargs):
        query = request.GET.get("query").upper()
        try: 
            predio = Predio.objects.get(claveCatastral=query)
            
        except ObjectDoesNotExist:
            messages.error(request, 'xd')
            return render(request, "personal/pago/historial_pagados.html")
        
        field_name = 'idtipo'
        temp = Predio.objects.get(claveCatastral=query)
        field_object = Predio._meta.get_field(field_name)
        field_value = field_object.value_from_object(temp)
        
        field_name2 = 'costo'
        temp2 = TipoPredio.objects.get(id=field_value)
        field_object2 = TipoPredio._meta.get_field(field_name2)
        field_value2 = field_object2.value_from_object(temp2)
        
        costoP=field_value2
        
        #Fecha de Pago
        time = datetime.now()
        date = time.strftime('%d/%m/%Y')
                    
        form = pagoForm(claveCatastral=predio, monto=costoP, fechaPago=date)
        
        
        
       
        context={
        "form": form,
        "title" : 'Cobrar',
        "entity" : 'Pagos',
        "action": 'add',
        "query": query,
        "tasabase": costoP,
        
        }


        return render(request, self.template_name, context=context)

    def get_success_url(self, request, **kwargs):
        
        try: 
            query = request.GET.get("query").upper()
            predio = Predio.objects.get(claveCatastral=query)
            claveCatastral = predio.claveCatastral
            success_url = "/personal/predial/pago/historial_pagados?buscar{claveCatastral}"
        except ObjectDoesNotExist:
            messages.error(request, 'xd')
            return render(request, "personal/pago/historial_pagados.html")
            
        return success_url
    
    def post(self, request, *args, **kwargs):
        data = {}
        
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)   
    
    
"""Vistas del Timbrado de Predial"""

def Lista_facturas_predial(request):
    url = "http://devfactura.in/api/v4/cfdi40/list"
    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'F-PLUGIN': '9d4095c8f7ed5785cb14c0e3b033eeb8252416ed',
    'F-Api-Key': 'JDJ5JDEwJHpuam0yVlp2MnlVNmJqVGFJUmppSXU1VlQ1bXpCUkFGeXNmMlpXM1VhbE9xVWlJVnp1V002',
    'F-Secret-Key': 'JDJ5JDEwJDRMUmFncEFCNmwyWWhYemZpZmdOY3VBVXdXSmM2a3NMb25DVjlTQktUa05yMlRZTmFXMDVH'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    #print(type(response))
    decode_json = response.json()
    #print(response.text)
    return render(request,'factura/list_factura.html',{'data':decode_json['data']})

def TimbrarPredial(request):

    url = "http://devfactura.in/api/v4/cfdi40/create"
    
    payload = json.dumps({
    "Receptor": {
        "UID": "62d9cafd1c465"
    },
    "TipoDocumento": "factura",
    "Conceptos": [
        {
        "ClaveProdServ": "01010101",
        "Cantidad": 1,
        "ClaveUnidad": "E48",
        "Unidad": "Unidad de servicio",
        "ValorUnitario": 1.0,
        "Descripcion": "Pago de Prueba 4.0",
        "Impuestos": {
            "Traslados": [
            {
                "Base": 1.16,
                "Impuesto": "002",
                "TipoFactor": "Tasa",
                "TasaOCuota": "0.00",
                "Importe": 0.00
            }
            ],
            "Locales": [
            {
                "Base": 1.00,
                "Impuesto": "ISH",
                "TipoFactor": "Tasa",
                "TasaOCuota": "0.160000",
                "Importe": 0.16
            }
            ]
        }
        }
    ],
    "UsoCFDI": "S01",
    "Serie": 19963,
    "FormaPago": "01",
    "MetodoPago": "PUE",
    "Moneda": "MXN",
    "EnviarCorreo": True
    })
    
    headers = {
    'Content-Type': 'application/json',
    'F-PLUGIN': '9d4095c8f7ed5785cb14c0e3b033eeb8252416ed',
    'F-Api-Key': 'JDJ5JDEwJHpuam0yVlp2MnlVNmJqVGFJUmppSXU1VlQ1bXpCUkFGeXNmMlpXM1VhbE9xVWlJVnp1V002',
    'F-Secret-Key': 'JDJ5JDEwJDRMUmFncEFCNmwyWWhYemZpZmdOY3VBVXdXSmM2a3NMb25DVjlTQktUa05yMlRZTmFXMDVH'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text)
    return render(request, 'personal/timbrado/timbrado.html')

class timbradoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    permission_required = 'predial.view_pago'
    model = Pago
    template_name = 'personal/timbrado/timbrado_list.html'

    """ @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) """
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Timbrados'
        context['create_url'] = reverse_lazy('predial:pago_add')
        
        
        return context
    
    def get_queryset(self):
        object_list = Pago.objects.filter(status_pagado = True)
        return object_list

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = Pago.objects.get(pk = request.POST['id']).toJSON().order_by('fechaPago')
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data) 

class Timbrar(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = 'predial.view_predio','predial.view_contribuyente'
    template_name = 'personal/timbrado/timbrar.html'
    model = Pago
    form_class = RespuestaForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            
            if action == 'edit':
                form = self.get_form()
                data = form.save()
                
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) 
   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Timbrar'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('predial:timbrado_list')
        
        return context 

""" Vistas de la seccion Reportes """

class ReportesPagoView(TemplateView):
    template_name= 'personal/reportes/reporte_pago.html'
   
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Pagos'
        context['form'] = ReportForm
        return context
    
    def post(self, request, *args, **kwargs):
        
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = {}
                start_date = request.POST.get('start_date','')
                print ("fechaInicio: ",start_date)
                end_date = request.POST.get('end_date','')
                print ("fechafinal: ",end_date)
                search = Pago.objects.all()
                
                if len(start_date) and len(end_date):
                    search = search.filter(fechaPago__range=[start_date, end_date], status_pagado=True).values()
                print ("Datos Filtrados: ",search)
                data = [entry for entry in search]
                print("xD:", data)
                    
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data, safe=False)
    

"""contributente 2.0 xd"""

class informacionPredio (TemplateView):
    template_name = "contribuyente/predio_info_cont.html"
    id = id
    def get(self, request, id, **kwargs):
        objectlist = Predio.objects.filter(id=id)
        context={
        "object_list":objectlist,

        }
        return render(request, self.template_name, context=context)



def pagoCont(request):

    #Validacion de Usuario
    user = request.user
    if not user.is_authenticated:
        return redirect('/contribuyente')

    #Buscar en base a la clave catastral
    pago_obj = {}
    predio= None
    query = None
    try:
        query = request.GET.get("query").upper()  
             
    except ValueError:
        print('Invalid Value')
    
    try:
        
        pago_obj = Pago.objects.filter(claveCatastral=query).order_by('agnio')
        
    except ValueError:
        messages.error(request, 'Has ingresado un valor invalido')
        
    try:
        predio = Predio.objects.get(claveCatastral=query)
                
    except ObjectDoesNotExist:
            if query != None:
                messages.error(request, 'No existe ese Predio')
                return render(request, "contribuyente/predio_info.html")

    context={
        "object_list" : pago_obj,
        "query" : query,
        "predio": predio,
        
    }

    return render(request, 'contribuyente/pago/historial.html', context=context)



""" class pagoCreateViewCont(CreateView):
    form_class = pagoForm
    model = Pago
    template_name = 'contribuyente/pago/pago_add.html'
    success_url =  reverse_lazy('usuario:usuario_info')
    

    def get(self, request, **kwargs):
        query = request.GET.get("query").upper()
        try: 
            predio = Predio.objects.get(claveCatastral=query)
            
        except ObjectDoesNotExist:
            messages.error(request, 'xd')
            return render(request, "usuario/usuario_info.html")
        
        field_name = 'idtipo'
        temp = Predio.objects.get(claveCatastral=query)
        field_object = Predio._meta.get_field(field_name)
        field_value = field_object.value_from_object(temp)
        
        field_name2 = 'costo'
        temp2 = TipoPredio.objects.get(id=field_value)
        field_object2 = TipoPredio._meta.get_field(field_name2)
        field_value2 = field_object2.value_from_object(temp2)
        
        costoP=field_value2
        
                    
        form = pagoForm(claveCatastral=predio, monto=costoP)
        
        context={
        "form": form,
        "title" : 'Cobrar',
        "entity" : 'Pagos',
        "action": 'add',
        "tasabase": costoP,
        "list_url": reverse_lazy('predial:historial'),
        

        }


        return render(request, self.template_name, context=context)

    
    
    def post(self, request, *args, **kwargs):
        data = {}
        
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

 """


class pagoUpdateViewCont(LoginRequiredMixin, UpdateView):
    form_class = pagoFormCont
    model = Pago
    template_name = 'contribuyente/pago/pago_add.html'
    success_url =  reverse_lazy('predial:historialCont')
    
    def get(self, request, **kwargs):
        claveCatastral = self.object.claveCatastral
        print ("a: ",claveCatastral)
        agnio = self.object.agnio
        print ("agnio: ",agnio)
        try: 
            predio = Predio.objects.get(claveCatastral=claveCatastral)
            
        except ObjectDoesNotExist:
            messages.error(request, 'xd')
            return render(request, "contribuyente/pago/historial.html")
        
        field_name = 'idtipo'
        temp = Predio.objects.get(claveCatastral=claveCatastral)
        field_object = Predio._meta.get_field(field_name)
        field_value = field_object.value_from_object(temp)
        
        field_name2 = 'costo'
        temp2 = TipoPredio.objects.get(id=field_value)
        field_object2 = TipoPredio._meta.get_field(field_name2)
        field_value2 = field_object2.value_from_object(temp2)
        
        costoP=field_value2
        
        #Fecha de Pago
        time = datetime.now()
        date = time.strftime('%d/%m/%Y')
                    
        form = pagoForm(claveCatastral=predio, monto=costoP, fechaPago=date, agnio=agnio)
    
       
        context={
        "form": form,
        "title" : 'Cobrar',
        "entity" : 'Pagos',
        "action": 'edit',
        "query": claveCatastral,
        "tasabase": costoP,
        
        }


        return render(request, self.template_name, context=context)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            
            if action == 'edit':
                form = self.get_form()
                
                data = form.save()
                
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False) 
     

    



    