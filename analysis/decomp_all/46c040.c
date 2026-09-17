
void FUN__text__0046c040(int param_1,char param_2)

{
  ushort uVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (((param_2 < '\0') || ('\t' < param_2)) &&
     (iVar3 = FUN__text__00424f80("(0<=dir)&&(dir<=9)",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618c04 + 1,0), iVar3 != 0)) {
    pcVar2 = (code *)swi(3);
    (*pcVar2)();
    return;
  }
  uVar1 = *(ushort *)(*(int *)(param_1 + 600) + 2);
  local_c = uVar1 - 0x183;
  switch(uVar1) {
  case 0x183:
  case 0x184:
  case 0x185:
  case 0x186:
  case 0x187:
  case 0x188:
  case 0x189:
  case 0x18a:
  case 0x18b:
  case 0x18c:
  case 0x18d:
  case 0x18e:
  case 399:
  case 400:
  case 0x191:
  case 0x192:
  case 0x193:
  case 0x194:
  case 0x195:
  case 0x196:
  case 0x19b:
  case 0x19c:
  case 0x19d:
  case 0x19e:
    FUN__text__0046c290(param_1);
    break;
  default:
    *(char *)(param_1 + 0x28a) = param_2;
  }
  local_8 = 0x46c0ee;
  FUN__text__0056ce80();
  return;
}

