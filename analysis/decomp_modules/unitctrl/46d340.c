
void FUN__text__0046d340(int param_1,int param_2,int param_3,undefined2 param_4)

{
  code *pcVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__0046a430(param_1);
  if (iVar2 == 0) {
    local_14 = FUN__text__0046a950(param_1);
    switch(local_14) {
    case 0:
      local_10 = 0xffff0000;
      break;
    case 1:
      local_10 = 0xffff4040;
      break;
    case 2:
      local_10 = 0xff8040ff;
      break;
    case 3:
      local_10 = 0xffffff80;
      break;
    case 4:
      local_10 = 0xff80ff40;
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618c1c + 0x26,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    local_c = (((*(short *)(*(int *)(param_1 + 600) + 0x16) * 100) /
               (int)*(short *)(*(int *)(param_1 + 600) + 0x14)) * 0x28) / 100;
    FUN__text__00410310(param_2 + -0x14,param_3 + 1,local_c,5,
                        CONCAT22((short)((uint)local_c >> 0x10),param_4),local_10,0);
    FUN__text__00410310(param_2 + -0x16,param_3,0x2c,7,CONCAT22(extraout_var,param_4),0xff202020,0);
  }
  else {
    iVar2 = ((*(short *)(*(int *)(param_1 + 600) + 0x16) * 100) /
            (int)*(short *)(*(int *)(param_1 + 600) + 0x14)) * 0x28;
    local_c = iVar2 / 100;
    FUN__text__00410310(param_2 + -0x14,param_3 + 1,local_c,2,
                        CONCAT22((short)((uint)(iVar2 % 100) >> 0x10),param_4),0xffff0000,0);
    iVar2 = ((*(short *)(*(int *)(param_1 + 600) + 0x1c) * 100) /
            (int)*(short *)(*(int *)(param_1 + 600) + 0x1a)) * 0x28;
    local_c = iVar2 / 100;
    FUN__text__00410310(param_2 + -0x14,param_3 + 4,local_c,2,
                        CONCAT22((short)((uint)(iVar2 % 100) >> 0x10),param_4),0xff00ff00,0);
    if (*(short *)(param_1 + 0x10) < 1) {
      if (0 < *(short *)(param_1 + 0xc)) {
        if (*(short *)(param_1 + 0xe) == 0) {
          local_c = 0;
        }
        else {
          local_c = (*(short *)(param_1 + 0xc) * 100) / (int)*(short *)(param_1 + 0xe);
        }
        iVar2 = (local_c * 0x28) / 100;
        local_c = 0x28 - iVar2;
        FUN__text__00410310(param_2 + -0x14,param_3 + 7,local_c,1,
                            CONCAT22((short)((uint)iVar2 >> 0x10),param_4),0xff00ffff,0);
      }
    }
    else {
      if (*(short *)(param_1 + 0x12) == 0) {
        local_c = 0;
      }
      else {
        local_c = (*(short *)(param_1 + 0x10) * 100) / (int)*(short *)(param_1 + 0x12);
      }
      iVar2 = local_c * 0x28;
      local_c = iVar2 / 100;
      FUN__text__00410310(param_2 + -0x14,param_3 + 7,local_c,1,
                          CONCAT22((short)((uint)(iVar2 % 100) >> 0x10),param_4),0xff00ffff,0);
    }
    FUN__text__00410310(param_2 + -0x16,param_3,0x2c,9,param_4,0xff202020,0);
  }
  local_8 = 0x46d67b;
  FUN__text__0056ce80();
  return;
}

