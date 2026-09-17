
int FUN__text__00528cd9(int param_1,undefined4 param_2,undefined4 param_3,int param_4,int param_5,
                       uint *param_6,undefined4 param_7,undefined4 param_8,undefined4 param_9)

{
  int iVar1;
  uint *puVar2;
  uint *puVar3;
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  uint local_64;
  uint local_60;
  uint local_5c;
  uint local_58 [6];
  undefined4 local_40;
  undefined4 local_3c;
  uint local_1c [4];
  uint local_c;
  uint local_8;
  
  FUN__text__0052b0a9();
  if (((param_1 == 0) || (param_4 == 0)) || (param_5 == 0)) {
LAB__text__00528d4c:
    iVar1 = -0x7789f794;
  }
  else {
    iVar1 = FUN__text__0052d4bb(param_4,param_5,param_9,1);
    if (iVar1 < 0) goto LAB__text__00528d51;
    iVar1 = 6;
    puVar2 = local_1c;
    if (param_6 == (uint *)0x0) {
      puVar2 = local_58;
      puVar3 = local_1c;
      for (; iVar1 != 0; iVar1 = iVar1 + -1) {
        *puVar3 = *puVar2;
        puVar2 = puVar2 + 1;
        puVar3 = puVar3 + 1;
      }
    }
    else {
      for (; iVar1 != 0; iVar1 = iVar1 + -1) {
        *puVar2 = *param_6;
        param_6 = param_6 + 1;
        puVar2 = puVar2 + 1;
      }
      if ((((local_64 < local_1c[2]) || (local_1c[2] < local_1c[0])) ||
          ((local_60 < local_1c[3] || ((local_1c[3] < local_1c[1] || (local_5c < local_8)))))) ||
         (local_8 < local_c)) goto LAB__text__00528d4c;
    }
    iVar1 = FUN__text__00527071(param_1,param_2,param_3,local_6c,local_70,local_40,local_3c,local_68
                                ,local_1c,param_7,param_8);
    if (-1 < iVar1) {
      iVar1 = 0;
    }
  }
LAB__text__00528d51:
  FUN__text__0052b0c2();
  return iVar1;
}

