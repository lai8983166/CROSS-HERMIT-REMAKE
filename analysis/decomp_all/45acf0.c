
void FUN__text__0045acf0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (DAT_007a49fc != 0) {
    local_c = param_1;
    if (param_1 == 0) {
      (*API_KERNEL32_DLL_lstrcpyA)
                (&DAT_007a46b0,
                 "D:\\Deverop\\Business\\Enter Brain\\Cross Hermit\\Game\\data\\sound\\nami.mp3");
      FUN__text__0056ce80();
    }
    else {
      if (param_1 != 1) goto LAB__text__0045ad84;
      (*API_KERNEL32_DLL_lstrcpyA)(&DAT_007a46b0,&DAT_0059aab8);
      FUN__text__0056ce80();
    }
    FUN__text__0041e140(&DAT_007a46b0);
  }
LAB__text__0045ad84:
  local_8 = 0x45ad91;
  FUN__text__0056ce80();
  return;
}

