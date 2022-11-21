from server.models import Basket


def basket_items_count(request):
    if request.user.is_authenticated:
        return {
            "basket_items": Basket.objects.filter(client=request.user).count()
        }
    return {
            "basket_items": "0"
        }