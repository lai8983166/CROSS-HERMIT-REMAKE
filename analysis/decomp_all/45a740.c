
/* WARNING: Removing unreachable block (ram,0x0045a8fc) */
/* WARNING: Removing unreachable block (ram,0x0045a90c) */
/* WARNING: Removing unreachable block (ram,0x0045a919) */
/* WARNING: Removing unreachable block (ram,0x0045a934) */
/* WARNING: Removing unreachable block (ram,0x0045a941) */
/* WARNING: Removing unreachable block (ram,0x0045a9ba) */
/* WARNING: Removing unreachable block (ram,0x0045a925) */
/* WARNING: Removing unreachable block (ram,0x0045a9f8) */
/* WARNING: Removing unreachable block (ram,0x0045aa14) */
/* WARNING: Removing unreachable block (ram,0x0045aa23) */
/* WARNING: Removing unreachable block (ram,0x0045aa3f) */
/* WARNING: Removing unreachable block (ram,0x0045aa4e) */
/* WARNING: Removing unreachable block (ram,0x0045aa6a) */
/* WARNING: Removing unreachable block (ram,0x0045aa77) */
/* WARNING: Removing unreachable block (ram,0x0045aa93) */
/* WARNING: Removing unreachable block (ram,0x0045aaa2) */
/* WARNING: Removing unreachable block (ram,0x0045aabb) */
/* WARNING: Removing unreachable block (ram,0x0045aacf) */
/* WARNING: Removing unreachable block (ram,0x0045aae2) */
/* WARNING: Removing unreachable block (ram,0x0045ab05) */
/* WARNING: Removing unreachable block (ram,0x0045ab86) */
/* WARNING: Removing unreachable block (ram,0x0045ab90) */
/* WARNING: Removing unreachable block (ram,0x0045ac58) */
/* WARNING: Removing unreachable block (ram,0x0045ac62) */
/* WARNING: Removing unreachable block (ram,0x0045ac7b) */
/* WARNING: Removing unreachable block (ram,0x0045ac85) */
/* WARNING: Removing unreachable block (ram,0x0045ac94) */

void FUN__text__0045a740(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_56c [16];
  int local_52c;
  undefined1 local_528 [1024];
  int local_128;
  undefined4 local_11c;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f998;
  local_10 = ExceptionList;
  puVar2 = local_56c;
  for (iVar1 = 0x157; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  FUN__text__004075e0();
  local_8 = CONCAT31(local_8._1_3_,1);
  local_11c = 0;
  local_128 = 0;
  do {
    iVar1 = FUN__text__004128f0(200,1);
    if (iVar1 != 0) {
      local_128 = local_128 + 1;
    }
    iVar1 = FUN__text__004128f0(0xd0,1);
    if (iVar1 != 0) {
      local_128 = local_128 + -1;
    }
    if (5 < local_128) {
      local_128 = 0;
    }
    if (local_128 < 0) {
      local_128 = 5;
    }
    iVar1 = FUN__text__004128f0(0x1c,1);
    if (iVar1 != 0) {
      local_52c = local_128;
      switch(local_128) {
      case 0:
        FUN__text__0045b9e0();
        break;
      case 1:
        FUN__text__0045b000();
        break;
      case 2:
        FUN__text__0045cef0();
        break;
      case 3:
        FUN__text__0045d2c0();
        break;
      case 4:
        FUN__text__0045d440();
        break;
      case 5:
        FUN__text__0045b5a0();
      }
    }
    FUN__text__0056d810(local_528,&DAT_0059aa94,(&PTR_s_Walk_Test_0060ce3c)[local_128]);
    FUN__text__00416370(200,0x100,0,local_528,0xffffffff);
    FUN__text__00422360(0);
  } while( true );
}

