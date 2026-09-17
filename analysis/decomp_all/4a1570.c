
void FUN__text__004a1570(void)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = local_c & 0xffff0000;
  FUN__text__0049f6c0(0);
  do {
    local_10 = (int)*(short *)(local_8 + 0x30);
    switch(local_10) {
    case 0:
      *(undefined2 *)(local_8 + 0x30) = 1;
      break;
    case 1:
      uVar1 = FUN__text__0049fd50();
      *(undefined2 *)(local_8 + 0x30) = uVar1;
      break;
    case 2:
      uVar1 = FUN__text__004a0760();
      *(undefined2 *)(local_8 + 0x30) = uVar1;
      break;
    case 3:
      uVar1 = FUN__text__004a0020();
      *(undefined2 *)(local_8 + 0x30) = uVar1;
      break;
    case 4:
      local_c = CONCAT22(local_c._2_2_,1);
    }
  } while ((local_c & 0xffff) == 0);
  FUN__text__00422360(0);
  if (DAT_007a4e62 == 0) {
    DAT_007a4e62 = 1;
    FUN__text__004ce210("Data\\Adv\\dat\\CH002.ybc",9);
    FUN__text__00439e30(6);
  }
  else {
    DAT_007e11a0 = 1;
    FUN__text__00439e30(9);
  }
  local_8 = 0x4a169c;
  FUN__text__0056ce80();
  return;
}

