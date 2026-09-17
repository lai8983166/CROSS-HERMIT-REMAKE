
void __fastcall FUN__text__0053b9b1(undefined4 *param_1)

{
  int *piVar1;
  
  *param_1 = &PTR_DAT_005d1154;
  if (param_1[0x12] != 0) {
    FUN__text__00548706();
    FUN__text__00548729();
  }
  if (param_1[2] != 0) {
    (*API_GDI32_DLL_DeleteObject)(param_1[2]);
  }
  piVar1 = (int *)param_1[0x13];
  if (piVar1 != (int *)0x0) {
    (**(code **)(*piVar1 + 8))(piVar1);
  }
  return;
}

