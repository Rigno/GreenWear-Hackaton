from django.shortcuts import render
from django.views.generic.list import ListView
from django.db.models import Q

from products.models import Product, Brand

# --- HOME PAGE --- #
def home(request):
    featured = Product.objects.order_by('?')[0:3]
            
    context = {
        'featured_products': featured,
    }
    return render(request, 'core/home.html', context)

# --- SHOP --- #
class Shop(ListView):
    model = Product
    template_name = "core/shop.html"
    context_object_name = "products"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sizes'] = Product.SIZES
        context['colors'] = Product.COLORS
        context['brands'] = Brand.objects.all()
        return context
    
    def get_queryset(self):
        search = self.request.GET.get('ricerca')
        order = self.request.GET.get('ordine')
        category = self.request.GET.get('categoria')
        minprice = self.request.GET.get('prezzo_min')
        maxprice = self.request.GET.get('prezzo_max')
        size = self.request.GET.get('taglia')
        color = self.request.GET.get('colore')
        brand = self.request.GET.get('marca')

        queryset = Product.objects.all()

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))

        if order:
            if order == 'nuovi':
                queryset = queryset.order_by('-data')
            elif order == 'sostenibili':
                queryset = queryset.order_by('footprint')
            elif order == 'prezzo_maggiore':
                queryset = queryset.order_by('-price')
            elif order == 'prezzo_minore':
                queryset = queryset.order_by('price')

        if category:
            queryset = queryset.filter(category__name__iexact=category)
            
        if minprice:
            queryset = queryset.filter(price__gte=float(minprice))
            
        if maxprice:
            queryset = queryset.filter(price__lte=float(maxprice))
            
        if size:
            queryset = queryset.filter(size=size)
            
        if color:
            colors = dict((name, value) for value, name in Product.COLORS)
            actual_color = colors.get(color)
            queryset = queryset.filter(color=actual_color)
            
        if brand:
            queryset = queryset.filter(brand__name=brand)
        
        return queryset
