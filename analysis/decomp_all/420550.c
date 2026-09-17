
void __thiscall
FUN__text__00420550(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    local_8 = param_1;
    (*API_GDI32_DLL_SelectObject)(param_1[2],param_1[3]);
    local_c = FUN__text__0056ce80();
    (*API_GDI32_DLL_BitBlt)
              (param_2,param_3,param_4,*(undefined4 *)(*local_8 + 4),*(undefined4 *)(*local_8 + 8),
               local_8[2],0,0,0xcc0020);
    FUN__text__0056ce80();
    (*API_GDI32_DLL_SelectObject)(local_8[2],local_c);
    FUN__text__0056ce80();
  }
  local_8 = (int *)0x420602;
  FUN__text__0056ce80();
  return;
}

