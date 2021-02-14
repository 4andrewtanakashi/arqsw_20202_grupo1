def getFigureDrawBounds():
    r = super.getFigDrawBounds()
    if getNodeCount() > 1:
        """Recomendação: Início da extração 1"""
        if START.get() != None:
            """Recomendação: Início da extração 4"""
            p1 = getPoint(0, 0)
            """Recomendação: Início da extração 2"""
            p2 = getPoint(1, 0)
            r.add(START.get().getBounds(p1, p2))
            """Recomendação: Fim da extração 4"""
            """Recomendação: Fim da extração 2"""
        if END.get() != None:
            """Recomendação: Início da extração 5"""
            p1 = getPoint(getNodeCount() - 1, 0)
            """Recomendação: Início da extração 3"""
            p2 = getPoint(getNodeCount() - 2, 0)
            r.add(END.get().getBounds(p1, p2))
            """Recomendação: Fim da extração 5"""
            """Recomendação: Fim da extração 3"""
        """Recomendação: Fim da extração 1"""
    return r
