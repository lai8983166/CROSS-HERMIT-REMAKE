
void FUN__text__0054e278(int param_1)

{
  int iVar1;
  char cVar2;
  
  iVar1 = *(int *)(param_1 + 0x184);
  if (*(int *)(iVar1 + 0x10) != 0) {
    if (*(char *)(param_1 + 0x49) != '\0') {
      cVar2 = FUN__text__0054dc78();
      if (cVar2 != '\0') {
        *(undefined1 **)(iVar1 + 0xc) = &LAB__text__0054dd5b;
        goto LAB__text__0054e2a9;
      }
    }
    *(code **)(iVar1 + 0xc) = FUN__text__0054db12;
  }
LAB__text__0054e2a9:
  *(undefined4 *)(param_1 + 0x88) = 0;
  return;
}

