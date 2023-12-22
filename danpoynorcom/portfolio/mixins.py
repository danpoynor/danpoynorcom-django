class PrevNextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ensure self.object and self.model are not None
        if self.object is None or self.model is None:
            return context

        # Get the current object
        current_object = self.object

        # Get the previous object
        previous_object = self.model.objects.filter(id__lt=current_object.id).order_by('-id').first()
        if previous_object is None:
            # If there is no previous object, get the last object
            previous_object = self.model.objects.order_by('-id').first()

        # Get the next object
        next_object = self.model.objects.filter(id__gt=current_object.id).order_by('id').first()
        if next_object is None:
            # If there is no next object, get the first object
            next_object = self.model.objects.order_by('id').first()

        context['previous_object'] = previous_object
        context['next_object'] = next_object

        return context
