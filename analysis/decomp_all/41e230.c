
void __thiscall
FUN__text__0041e230(int *param_1,undefined4 param_2,int param_3,int param_4,int param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18 [3];
  undefined4 local_c;
  int *local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((((*param_1 != 0) && (param_1[1] != 0)) && (param_1[2] != 0)) &&
     (((param_1[3] != 0 && (param_1[4] != 0)) && (param_1[5] != 0)))) {
    param_1[0x92] = param_3;
    local_8 = param_1;
    iVar1 = FUN__text__0041db30(param_2);
    if (iVar1 == 0) {
      local_18[2] = param_4 * 1000;
      local_c = 0;
      local_18[0] = param_5 * 1000;
      local_18[1] = 0;
      (**(code **)(*(int *)local_8[2] + 0x38))(local_8[2],local_18 + 2,1,local_18,0);
      local_1c = FUN__text__0056ce80();
      if (local_1c < 0) {
        FUN__text__0041d040(local_1c);
      }
      else {
        FUN__text__0041d930(local_8[0x96],local_8[0x97]);
        FUN__text__0041da80(local_8[0x93]);
        FUN__text__0041e6b0();
        (**(code **)(*(int *)local_8[1] + 0x1c))(local_8[1]);
        local_20 = FUN__text__0056ce80();
        *(undefined1 *)((int)local_8 + 0x22) = 1;
        *(undefined1 *)((int)local_8 + 0x21) = 0;
        local_1c = local_20;
      }
    }
  }
  local_8 = (int *)0x41e3c0;
  FUN__text__0056ce80();
  return;
}

