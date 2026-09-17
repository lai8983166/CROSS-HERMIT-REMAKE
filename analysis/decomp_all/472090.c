
void __thiscall FUN__text__00472090(int param_1,int param_2,int param_3,short param_4)

{
  int iVar1;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((((-1 < param_2) && (param_2 < 0x1f)) && (-1 < param_3)) &&
     (((param_3 < 0x1f &&
       (local_c = param_3 * 0x1f + param_2, *(char *)(param_1 + local_c + 0x108f7c) != -1)) &&
      (((int)*(char *)(param_1 + local_c + 0x108f7c) <= (int)param_4 && (-1 < param_4 + -1)))))) {
    if ((int)*(char *)(param_1 + local_c + 0x108f7c) < (int)param_4) {
      *(undefined1 *)(param_1 + local_c + 0x108f7c) = (undefined1)param_4;
    }
    param_4 = param_4 + -1;
    local_8 = param_1;
    FUN__text__00472090(param_2,param_3 + -1,
                        CONCAT22((short)((uint)(param_1 + local_c) >> 0x10),param_4),2);
    FUN__text__00472090(param_2 + -1,param_3,CONCAT22(extraout_var,param_4),4);
    FUN__text__00472090(param_2 + 1,param_3,CONCAT22(extraout_var_00,param_4),6);
    FUN__text__00472090(param_2,param_3 + 1,CONCAT22(extraout_var_01,param_4),8);
  }
  local_8 = 0x4721c6;
  FUN__text__0056ce80();
  return;
}

