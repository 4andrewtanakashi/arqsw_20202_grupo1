# Generated from Java8Parser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Java8Parser import Java8Parser
else:
    from Java8Parser import Java8Parser

# This class defines a complete listener for a parse tree produced by Java8Parser.

TYPE = ["byte", "short", "int", "long", "float", "double", "char", "String", "boolean"]

class Java8ParserListener(ParseTreeListener):

    def __init__(self):
        self.dicionario = {}
        self.dicionario["type"] = []
        self.dicionario["imports"] = []
        self.dicionario["annotation"] = []
        self.nome_classe = ""


    # Enter a parse tree produced by Java8Parser#singleTypeImportDeclaration.
    def enterSingleTypeImportDeclaration(self, ctx:Java8Parser.SingleTypeImportDeclarationContext):
        self.dicionario["imports"].append(ctx.typeName().getText())

    # Enter a parse tree produced by Java8Parser#normalClassDeclaration.
    def enterNormalClassDeclaration(self, ctx:Java8Parser.NormalClassDeclarationContext):
        for child_class_dec in ctx.getChildren():
            if isinstance(child_class_dec, tree.Tree.TerminalNodeImpl) and child_class_dec.getText() != "class":
                self.dicionario["name_obj"] = child_class_dec.getText()
            if isinstance(child_class_dec, Java8Parser.ClassModifierContext):
                for child_class_modifier_ctx in child_class_dec.getChildren():
                    if isinstance(child_class_modifier_ctx, Java8Parser.AnnotationContext):
                        self.dicionario["annotation"].append(child_class_modifier_ctx.getText())


    # Enter a parse tree produced by Java8Parser#unannClassType.
    def enterUnannClassType(self, ctx:Java8Parser.UnannClassTypeContext):
        if not TYPE.__contains__(ctx.getText()):
            self.dicionario["type"].append(ctx.getText())

    # Enter a parse tree produced by Java8Parser#unannClassType_lf_unannClassOrInterfaceType.
    def enterUnannClassType_lf_unannClassOrInterfaceType(self, ctx:Java8Parser.UnannClassType_lf_unannClassOrInterfaceTypeContext):
        if not TYPE.__contains__(ctx.getText()):
            self.dicionario["type"].append(ctx.getText())


    # Exit a parse tree produced by Java8Parser#unannClassType_lfno_unannClassOrInterfaceType.
    def exitUnannClassType_lfno_unannClassOrInterfaceType(self, ctx:Java8Parser.UnannClassType_lfno_unannClassOrInterfaceTypeContext):
        if not TYPE.__contains__(ctx.getText()):
            self.dicionario["type"].append(ctx.getText())


    # Enter a parse tree produced by Java8Parser#unannTypeVariable.
    def enterUnannTypeVariable(self, ctx:Java8Parser.UnannTypeVariableContext):
        if not TYPE.__contains__(ctx.getText()):
            self.dicionario["type"].append(ctx.getText())

    # Enter a parse tree produced by Java8Parser#methodModifier.
    def enterMethodModifier(self, ctx:Java8Parser.MethodModifierContext):
        for child_methodMod_ctx in ctx.getChildren():
            if isinstance(child_methodMod_ctx, Java8Parser.AnnotationContext):
                if "annotation" not in self.dicionario:
                    self.dicionario["annotation"] = []
                self.dicionario["annotation"].append(child_methodMod_ctx.getText())

    # Enter a parse tree produced by Java8Parser#normalInterfaceDeclaration.
    def enterNormalInterfaceDeclaration(self, ctx:Java8Parser.NormalInterfaceDeclarationContext):
        for child_interface_dec in ctx.getChildren():
            print("child_interface_dec: ", child_interface_dec.getText())
            if isinstance(child_interface_dec, tree.Tree.TerminalNodeImpl) and child_interface_dec.getText() != "interface":
                print("Entrou aqui child_interface_dec")
                self.dicionario["name_obj"] = child_interface_dec.getText()
            if isinstance(child_interface_dec, Java8Parser.InterfaceModifierContext):
                for child_interface_modifier_ctx in child_interface_dec.getChildren():
                    if isinstance(child_interface_modifier_ctx, Java8Parser.AnnotationContext):
                        self.dicionario["annotation"].append(child_interface_modifier_ctx.getText())


    def enterEnumDeclaration(self, ctx:Java8Parser.EnumDeclarationContext):
        for child_enum_dec in ctx.getChildren():
            print("child_enum_dec.getText(): ", child_enum_dec.getText())
            if isinstance(child_enum_dec, tree.Tree.TerminalNodeImpl) and child_enum_dec.getText() != "enum":
                print("Entrou aqui child_enum_dec.getText()")
                self.dicionario["name_obj"] = child_enum_dec.getText()
            if isinstance(child_enum_dec, Java8Parser.ClassModifierContext):
                for child_enum_modifier_ctx in child_enum_dec.getChildren():
                    if isinstance(child_enum_modifier_ctx, Java8Parser.AnnotationContext):
                        self.dicionario["annotation"].append(child_enum_modifier_ctx.getText())

    # Enter a parse tree produced by Java8Parser#annotationTypeDeclaration.
    def enterAnnotationTypeDeclaration(self, ctx:Java8Parser.AnnotationTypeDeclarationContext):
        for child_interface_annotation_dec in ctx.getChildren():
            print("child_interface_annotation_dec.getText(): ", child_interface_annotation_dec.getText())
            if isinstance(child_interface_annotation_dec, tree.Tree.TerminalNodeImpl)  and (child_interface_annotation_dec.getText() != '@' and child_interface_annotation_dec.getText() != "interface"):
                print("child_interface_annotation_dec")
                self.dicionario["name_obj"] = child_interface_annotation_dec.getText()
            if isinstance(child_interface_annotation_dec, Java8Parser.InterfaceModifierContext):
                for child_interface_annotation_modifier_ctx in child_interface_annotation_dec.getChildren():
                    if isinstance(child_interface_annotation_modifier_ctx, Java8Parser.AnnotationContext):
                        self.dicionario["annotation"].append(child_interface_annotation_modifier_ctx.getText())
