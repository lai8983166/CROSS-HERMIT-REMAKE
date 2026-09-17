
void __thiscall FUN__text__00423950(int param_1,undefined4 param_2,undefined4 *param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [7];
  undefined4 uStack_2c;
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  (*API_GDI32_DLL_BitBlt)
            (param_2,*param_3,param_3[1],param_3[2],param_3[3],*(undefined4 *)(param_1 + 8),0,0,
             0xcc0020);
  FUN__text__0056ce80();
  uStack_2c = 0x4239ba;
  FUN__text__0056ce80();
  return;
}

