
int __thiscall FUN__text__0053b9f8(int param_1,int *param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_retaddr;
  
  if ((param_2 == (int *)0x0) || (param_3 == 0)) {
    iVar1 = -0x7789f794;
  }
  else {
    iVar1 = FUN__text__00548d89(param_2,param_1 + 0x48);
    if (-1 < iVar1) {
      iVar1 = (*API_GDI32_DLL_CreateFontIndirectA)(param_3);
      *(int *)(param_1 + 8) = iVar1;
      if (iVar1 == 0) {
        iVar1 = -0x7ff8fff2;
      }
      else {
        *(int **)(param_1 + 0x4c) = param_2;
        (**(code **)(*param_2 + 4))(param_2);
        puVar2 = (undefined4 *)(param_1 + 0xc);
        for (iVar1 = 0xf; iVar1 != 0; iVar1 = iVar1 + -1) {
          *puVar2 = *unaff_retaddr;
          unaff_retaddr = unaff_retaddr + 1;
          puVar2 = puVar2 + 1;
        }
        iVar1 = 0;
      }
    }
  }
  return iVar1;
}

