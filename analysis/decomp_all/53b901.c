
undefined4 __fastcall FUN__text__0053b901(int *param_1)

{
  if (*param_1 != 0) {
    (*API_GDI32_DLL_DeleteObject)(*param_1);
  }
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  return 0;
}

