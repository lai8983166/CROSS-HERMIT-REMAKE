
void __fastcall FUN__text__0053d339(undefined4 *param_1)

{
  int *piVar1;
  
  *param_1 = &PTR_DAT_005d11d0;
  FUN__text__0053d0f6(param_1);
  piVar1 = (int *)param_1[2];
  if (piVar1 != (int *)0x0) {
    (**(code **)(*piVar1 + 8))(piVar1);
    param_1[2] = 0;
  }
  return;
}

