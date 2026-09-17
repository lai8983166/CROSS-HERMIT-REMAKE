
void FUN__text__0046d6a0(int param_1,short param_2,short param_3)

{
  ushort uVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  iVar3 = FUN__text__00469ad0(param_1);
  if ((iVar3 != 0) || (iVar3 = FUN__text__00469c60(param_1), iVar3 != 0)) {
    uVar1 = *(ushort *)(*(int *)(param_1 + 600) + 2);
    local_18 = uVar1 - 0x183;
    switch(uVar1) {
    case 0x183:
    case 0x184:
    case 0x185:
    case 0x186:
    case 0x187:
    case 0x188:
    case 399:
    case 400:
    case 0x191:
    case 0x192:
    case 0x193:
    case 0x194:
      local_c = 0xff80ff00;
      local_10 = -8;
      break;
    case 0x189:
    case 0x18a:
    case 0x18b:
    case 0x18c:
    case 0x18d:
    case 0x18e:
    case 0x195:
    case 0x196:
      local_c = 0xff80ff00;
      local_10 = 0x1e;
      break;
    default:
      iVar3 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618c20 + 0x26,0);
      if (iVar3 != 0) {
        pcVar2 = (code *)swi(3);
        (*pcVar2)();
        return;
      }
    }
    iVar3 = FUN__text__00468d80(param_1);
    if (iVar3 == 0) {
      local_14 = (*(short *)(param_1 + 0x4fe) * 100) / 600;
    }
    else {
      local_14 = (*(short *)(param_1 + 0x4fe) * 100) / 900;
    }
    local_14 = (local_14 * 0x3c) / 100;
    FUN__text__00410310(param_2 + -0x1e,(short)(param_3 + -0x50) + 1 + local_10,local_14,7,0x37a,
                        local_c,0);
    FUN__text__00410310(param_2 + -0x20,(short)(param_3 + -0x50) + local_10,0x40,9,0x37a,0xff202020,
                        0);
  }
  local_8 = 0x46d838;
  FUN__text__0056ce80();
  return;
}

