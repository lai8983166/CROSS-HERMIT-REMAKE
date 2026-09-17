
undefined4 FUN_00585ca0(undefined4 param_1,undefined2 param_2)

{
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 uVar2;
  undefined4 uVar1;
  bool bVar3;
  
  (*API_KERNEL32_DLL_InterlockedIncrement)(&DAT_0080bb6c);
  bVar3 = DAT_0080bb68 == 0;
  uVar2 = extraout_var;
  if (!bVar3) {
    (*API_KERNEL32_DLL_InterlockedDecrement)(&DAT_0080bb6c);
    FUN_00577040(0x13);
    uVar2 = extraout_var_00;
  }
  uVar1 = FUN_00585d20(param_1,CONCAT22(uVar2,param_2));
  if (bVar3) {
    (*API_KERNEL32_DLL_InterlockedDecrement)(&DAT_0080bb6c);
  }
  else {
    FUN_005770e0(0x13);
  }
  return uVar1;
}

