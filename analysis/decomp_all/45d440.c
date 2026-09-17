
/* WARNING: Removing unreachable block (ram,0x0045d5d5) */

void FUN__text__0045d440(void)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__004150a0(0);
  FUN__text__004143a0(0,0,0xff);
  FUN__text__00415ed0(local_8 + 0x30,&DAT_0059adc8,1,1);
  local_c = 0;
  local_10 = 1;
  do {
    local_c = local_c + local_10;
    if (0x1fe < local_c) {
      local_10 = -local_10;
    }
    if (local_c < 1) {
      local_10 = -local_10;
    }
    if (0x100 < local_c) {
      local_14._0_1_ = (char)local_c;
      if (0xff < local_c + -0x100) {
        local_14._0_1_ = 0xff;
      }
      FUN__text__00410310(0,0,0x400,0x300,0,local_14 << 0x18 | 0xff8060,1);
    }
    if (local_c < 0x100) {
      cVar1 = -1 - (char)local_c;
      local_14 = CONCAT31(local_14._1_3_,cVar1);
      if (cVar1 == '\0') {
        local_14 = CONCAT31(local_14._1_3_,1);
      }
      FUN__text__00410310(0,0,0x400,0x300,0,local_14 << 0x18,1);
    }
    *(undefined2 *)(local_8 + 0xa6) = 1;
    FUN__text__004079c0(0,0);
    FUN__text__00422360(0);
  } while( true );
}

