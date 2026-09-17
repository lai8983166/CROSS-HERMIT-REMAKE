
void FUN__text__00457730(undefined4 param_1,undefined4 param_2,undefined2 param_3,int param_4,
                        undefined *param_5)

{
  int iVar1;
  undefined2 extraout_var;
  undefined4 *puVar2;
  undefined4 local_250 [16];
  undefined *local_210;
  undefined *local_20c;
  undefined1 local_208 [512];
  undefined4 local_8;
  
  puVar2 = local_250;
  for (iVar1 = 0x93; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_5 == (undefined *)0x0) {
    local_210 = &DAT_005953ac;
  }
  else {
    local_210 = param_5;
  }
  local_20c = local_210;
  FUN__text__0056d810(local_208,"%s:%d",local_210,*(undefined4 *)(param_4 + 0x18),
                      *(undefined4 *)(param_4 + 0x1c));
  FUN__text__0040ec50(param_1,param_2,CONCAT22(extraout_var,param_3),0xffff0000,0,local_208);
  local_8 = 0x4577dc;
  FUN__text__0056ce80();
  return;
}

