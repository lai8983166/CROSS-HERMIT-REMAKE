
void __fastcall FUN__text__005491b2(undefined4 *param_1)

{
  int iVar1;
  
  iVar1 = param_1[3];
  *param_1 = &PTR_DAT_005d3224;
  if (iVar1 != 0) {
    param_1[3] = iVar1 - (uint)*(byte *)(iVar1 + -1);
  }
  FUN__text__005490e1();
  return;
}

