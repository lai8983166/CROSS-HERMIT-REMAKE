
void FUN__text__0043b110(int param_1,int param_2,int param_3,int param_4,int param_5,short param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((((-1 < param_4) && (param_4 <= param_2 + -1)) && (-1 < param_5)) &&
     ((param_5 <= param_3 + -1 &&
      (*(short *)(param_1 + (param_5 * param_2 + param_4) * 2) < param_6)))) {
    *(short *)(param_1 + (param_5 * param_2 + param_4) * 2) = param_6;
    FUN__text__0043b110(param_1,param_2,param_3,param_4 + -1,param_5,param_6 + -1);
    FUN__text__0043b110(param_1,param_2,param_3,param_4 + 1,param_5,param_6 + -1);
    FUN__text__0043b110(param_1,param_2,param_3,param_4,param_5 + -1,param_6 + -1);
    FUN__text__0043b110(param_1,param_2,param_3,param_4,param_5 + 1,param_6 + -1);
  }
  local_8 = 0x43b23f;
  FUN__text__0056ce80();
  return;
}

