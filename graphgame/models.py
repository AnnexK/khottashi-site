from django.db import models

# Create your models here.


class Vertex(models.Model):
    # координаты
    x = models.IntegerField('x coordinate')
    y = models.IntegerField('y coordinate')
    g = models.ForeignKey('Graph', models.CASCADE)

    def __str__(self):
        return f'({self.x}; {self.y})'

    def create_edge(self, v):
        if self.g != v.g:
            raise ValueError('vertices not in same graph')
        E = Edge(start=self,
                 end=v,
                 g=self.g)
        E.save()

    def delete_edge(self, w):
        e = Edge.objects.get(start=self, end=w)
        e.delete()

    def adjacent(self):
        return Edge.objects.filter(start=self)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['x', 'y'],
                                    name='pair of coords')
        ]


class Edge(models.Model):
    g = models.ForeignKey('Graph', models.CASCADE)

    # для какой вершины ребро является начальным
    start = models.ForeignKey('Vertex', models.CASCADE,
                              related_name='starts',
                              null=True)
    # для какой вершины ребро является конечным
    end = models.ForeignKey('Vertex', models.CASCADE,
                            related_name='ends',
                            null=True)

    def __str__(self):
        return f'<{self.start}, {self.end}>'


class Graph(models.Model):
    name = models.CharField('Graph name',
                            unique=True,
                            primary_key=True,
                            max_length=32)

    def __str__(self):
        return f'''Name: {self.name}
        Vertices: {list(v for v in self.vertex_set.all())}
        Edges: {list(e for e in self.edge_set.all())}'''

    def add_vertex(self, x, y):
        v = Vertex(x=x, y=y, g=self)
        v.save()

    def remove_vertex(self, x, y):
        v = self.get_vertex(x, y)
        v.delete()

    def get_vertex(self, x, y):
        return self.vertex_set.get(x=x, y=y)

    def add_edge(self, v, w):
        if (v not in self.vertex_set.all() or w not in self.vertex_set.all()):
            raise ValueError('vertices not in graph')

        if v is w:
            raise ValueError('loops are prohibited')

        e = Edge.objects.filter(start__exact=v,
                                end__exact=w)
        if e.exists():
            raise ValueError('edge already exists')

        v.create_edge(w)
        w.create_edge(v)

    def remove_edge(self, v, w):
        if (v not in self.vertex_set.all() or w not in self.vertex_set.all()):
            raise ValueError('vertices not in graph')

        v.delete_edge(w)
        w.delete_edge(v)

    def to_dict(self):
        verts = [v for v in self.vertex_set.all()]

        def edge(e: Edge):
            start = verts.index(e.start)
            end = verts.index(e.end)
            return (start, end)

        dct = {'name': self.name,
               'verts': [(v.x, v.y) for v in verts],
               'edges': [edge(e) for e in self.edge_set.all()]}

        return dct
