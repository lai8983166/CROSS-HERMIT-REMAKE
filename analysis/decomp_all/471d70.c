
void __thiscall FUN__text__00471d70(int param_1,int param_2,int param_3,short param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  _memset((void *)(param_1 + 0x108f7c),0,0x3c1);
  for (local_c = 0; local_c != 0xfa; local_c = local_c + 1) {
    if ((*(short *)(local_8 + 0x80aec + local_c * 0x520) != 0) && (local_c != param_3)) {
      local_1c = (int)((*(int *)(param_2 + 0x2ec) >> 0x10) +
                      (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_20 = (int)((*(int *)(param_2 + 0x2f0) >> 0x10) +
                      (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      iVar1 = *(int *)(local_8 + 0x80dd8 + local_c * 0x520);
      local_24 = (int)((iVar1 >> 0x10) + (iVar1 >> 0x1f & 0x1fU)) >> 5;
      iVar1 = *(int *)(local_8 + 0x80ddc + local_c * 0x520);
      local_28 = (int)((iVar1 >> 0x10) + (iVar1 >> 0x1f & 0xfU)) >> 4;
      local_14 = local_24 - local_1c;
      local_18 = local_28 - local_20;
      iVar1 = FUN__text__0056db00(local_14);
      if (iVar1 < 0x10) {
        iVar1 = FUN__text__0056db00(local_18);
        if (iVar1 < 0x10) {
          local_10 = (local_18 + 0xf) * 0x1f + 0xf + local_14;
          *(undefined1 *)(local_8 + local_10 + 0x108f7c) = 0xff;
        }
      }
    }
  }
  FUN__text__00471f50(param_2,param_3);
  FUN__text__00472090(0xf,0x10,param_4 + -1,2);
  FUN__text__00472090(0xf,0xe,param_4 + -1,8);
  FUN__text__00472090(0x10,0xf,param_4 + -1,6);
  FUN__text__00472090(0xe,0xf,param_4 + -1,4);
  FUN__text__00471070(param_2,param_3,(int)param_4);
  local_8 = 0x471f45;
  FUN__text__0056ce80();
  return;
}

